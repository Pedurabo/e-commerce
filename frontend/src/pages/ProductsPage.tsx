import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import mlProductsService, { MLProduct } from '../services/mlProductsService'

// Analytics tracking
const trackEvent = (eventName: string, data: any) => {
  console.log(`[Analytics] ${eventName}:`, data)
  // In a real app, this would send to analytics service
  localStorage.setItem(`analytics_${Date.now()}`, JSON.stringify({
    event: eventName,
    data,
    timestamp: new Date().toISOString()
  }))
}

const ProductsPage = () => {
  const { isAuthenticated, hasPremiumAccess } = useAuth()
  const navigate = useNavigate()
  const [selectedCategory, setSelectedCategory] = useState("All")
  const [sortBy, setSortBy] = useState("featured")
  const [priceRange, setPriceRange] = useState([0, 3000])
  const [searchQuery, setSearchQuery] = useState("")
  const [showFilters, setShowFilters] = useState(false)
  const [showReport, setShowReport] = useState(false)
  const [showFeedback, setShowFeedback] = useState(false)
  const [selectedProduct, setSelectedProduct] = useState<MLProduct | null>(null)
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [products, setProducts] = useState<MLProduct[]>([])
  const [pagination, setPagination] = useState({
    page: 1,
    limit: 12,
    total: 0,
    pages: 0
  })
  const [analytics, setAnalytics] = useState({
    pageViews: 0,
    productClicks: 0,
    cartAdds: 0,
    filterUses: 0
  })

  // Categories for filtering
  const categories = ["All", "Electronics", "Fashion", "Home & Garden", "Sports & Outdoors", "Books & Media", "Health & Beauty"]

  // Load products from ML service
  useEffect(() => {
    loadProducts()
  }, [page, selectedCategory, searchQuery, sortBy])

  const loadProducts = async () => {
    setLoading(true)
    try {
      const response = await mlProductsService.getLimitlessProducts({
        page,
        limit: 12,
        category: selectedCategory === "All" ? undefined : selectedCategory,
        search: searchQuery || undefined,
        sort_by: sortBy,
        sort_order: sortBy === "price-low" ? "asc" : "desc"
      })
      
      setProducts(response.products)
      setPagination(response.pagination)
      
      // Track page view
      setAnalytics(prev => ({ ...prev, pageViews: prev.pageViews + 1 }))
      trackEvent('page_view', { page: 'products', timestamp: new Date().toISOString() })
      
    } catch (error) {
      console.error('Failed to load products:', error)
      toast.error('Failed to load products. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleCategoryChange = (category: string) => {
    setSelectedCategory(category)
    setPage(1)
    setAnalytics(prev => ({ ...prev, filterUses: prev.filterUses + 1 }))
    trackEvent('filter_change', { filter: 'category', value: category })
  }

  const handleSortChange = (sort: string) => {
    setSortBy(sort)
    trackEvent('sort_change', { sort })
  }

  const handleProductClick = (product: MLProduct) => {
    setSelectedProduct(product)
    setAnalytics(prev => ({ ...prev, productClicks: prev.productClicks + 1 }))
    trackEvent('product_click', { productId: product.id, productName: product.name })
  }

  const handleViewModeChange = (mode: 'grid' | 'list') => {
    setViewMode(mode)
    trackEvent('view_mode_change', { mode })
  }

  const handleAddToCart = (product: MLProduct) => {
    if (!isAuthenticated) {
      toast.error('Please sign in to add items to cart')
      trackEvent('cart_add_failed', { reason: 'not_authenticated', productId: product.id })
      return
    }

    if (!hasPremiumAccess()) {
      toast.error('Premium membership required to use the cart')
      navigate('/account?tab=premium')
      trackEvent('cart_add_failed', { reason: 'no_premium', productId: product.id })
      return
    }

    // Get existing cart from localStorage
    const existingCart = localStorage.getItem('cart')
    const cartItems = existingCart ? JSON.parse(existingCart) : []

    // Check if product already exists in cart
    const existingItem = cartItems.find((item: any) => item.id === product.id)
    
    if (existingItem) {
      // Update quantity
      const updatedCart = cartItems.map((item: any) =>
        item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
      )
      localStorage.setItem('cart', JSON.stringify(updatedCart))
      toast.success('Quantity updated in cart')
      trackEvent('cart_update', { productId: product.id, newQuantity: existingItem.quantity + 1 })
    } else {
      // Add new item
      const newItem = {
        id: product.id,
        name: product.name,
        price: product.price,
        quantity: 1,
        image: product.images[0]
      }
      const updatedCart = [...cartItems, newItem]
      localStorage.setItem('cart', JSON.stringify(updatedCart))
      toast.success('Added to cart')
      trackEvent('cart_add', { productId: product.id, productName: product.name, price: product.price })
    }

    setAnalytics(prev => ({ ...prev, cartAdds: prev.cartAdds + 1 }))
  }

  const handleQuickView = (product: MLProduct) => {
    setSelectedProduct(product)
    trackEvent('quick_view', { productId: product.id, productName: product.name })
  }

  const handleWishlist = (product: MLProduct) => {
    const wishlist = JSON.parse(localStorage.getItem('wishlist') || '[]')
    const exists = wishlist.find((item: any) => item.id === product.id)
    
    if (exists) {
      const updatedWishlist = wishlist.filter((item: any) => item.id !== product.id)
      localStorage.setItem('wishlist', JSON.stringify(updatedWishlist))
      toast.success('Removed from wishlist')
      trackEvent('wishlist_remove', { productId: product.id })
    } else {
      const updatedWishlist = [...wishlist, { 
        id: product.id, 
        name: product.name, 
        price: product.price, 
        image: product.images[0] 
      }]
      localStorage.setItem('wishlist', JSON.stringify(updatedWishlist))
      toast.success('Added to wishlist')
      trackEvent('wishlist_add', { productId: product.id })
    }
  }

  const generateReport = () => {
    const report = {
      timestamp: new Date().toISOString(),
      totalProducts: pagination.total,
      currentPage: page,
      analytics: analytics,
      filters: {
        category: selectedCategory,
        sortBy,
        priceRange,
        searchQuery
      },
      topProducts: products
        .sort((a, b) => b.rating - a.rating)
        .slice(0, 5)
        .map(p => ({ id: p.id, name: p.name, rating: p.rating, price: p.price }))
    }
    
    console.log('Product Report:', report)
    trackEvent('report_generated', report)
    return report
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Enhanced Header with Glow Effects */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 via-purple-600/20 to-pink-600/20 animate-pulse"></div>
        <div className="container mx-auto px-4 py-12 relative z-10">
          <div className="text-center mb-8">
            <h1 className="text-5xl font-bold gradient-text mb-4 animate-fade-in">
              AI-Powered Products
            </h1>
            <p className="text-xl text-slate-300 mb-6 animate-slide-up">
              Discover limitless products with machine learning recommendations
            </p>
            <div className="flex justify-center space-x-4 animate-scale-in">
              <div className="pulse-glow px-4 py-2 rounded-full bg-blue-600/20 border border-blue-400/30">
                <span className="text-blue-300">🚀 ML-Powered</span>
              </div>
              <div className="pulse-glow px-4 py-2 rounded-full bg-purple-600/20 border border-purple-400/30">
                <span className="text-purple-300">✨ Limitless</span>
              </div>
              <div className="pulse-glow px-4 py-2 rounded-full bg-pink-600/20 border border-pink-400/30">
                <span className="text-pink-300">🎯 Smart</span>
              </div>
            </div>
          </div>
          
          {/* Enhanced Authentication Status Banner */}
          <div className="glass rounded-2xl p-6 mb-8 animate-fade-in">
            {isAuthenticated ? (
              hasPremiumAccess() ? (
                <div className="flex items-center justify-center text-green-300 bg-green-600/20 border border-green-400/30 rounded-xl p-4">
                  <span className="mr-3 text-2xl">✅</span>
                  <span className="text-lg font-medium">You're signed in with Premium access. You can add products to your cart!</span>
                </div>
              ) : (
                <div className="flex items-center justify-center text-yellow-300 bg-yellow-600/20 border border-yellow-400/30 rounded-xl p-4">
                  <span className="mr-3 text-2xl">⭐</span>
                  <span className="text-lg font-medium">
                    You're signed in but need Premium membership to use the cart. 
                    <button 
                      onClick={() => navigate('/account?tab=premium')} 
                      className="ml-2 underline font-medium hover:text-yellow-200 transition-colors"
                    >
                      Upgrade now
                    </button>
                  </span>
                </div>
              )
            ) : (
              <div className="flex items-center justify-center text-blue-300 bg-blue-600/20 border border-blue-400/30 rounded-xl p-4">
                <span className="mr-3 text-2xl">🔐</span>
                <span className="text-lg font-medium">
                  Sign in to add products to your cart. 
                  <button 
                    onClick={() => navigate('/login')} 
                    className="ml-2 underline font-medium hover:text-blue-200 transition-colors"
                  >
                    Sign in now
                  </button>
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 pb-12">
        {/* Enhanced Search and Toolbar */}
        <div className="glass rounded-2xl p-8 mb-8 animate-fade-in">
          <div className="flex flex-col lg:flex-row gap-6 items-center justify-between">
            {/* Enhanced Search Bar */}
            <div className="flex-1 max-w-md">
              <div className="relative group">
                <input
                  type="text"
                  placeholder="Search products..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="input w-full pl-12 pr-4 text-lg bg-slate-800/50 border-slate-600 focus:border-blue-400 focus:bg-slate-800/70"
                />
                <svg className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400 group-focus-within:text-blue-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>

            {/* Enhanced View Mode Toggle */}
            <div className="flex items-center space-x-2">
              <button
                onClick={() => handleViewModeChange('grid')}
                className={`p-3 rounded-xl transition-all duration-300 ${
                  viewMode === 'grid' 
                    ? 'bg-blue-600/30 text-blue-300 border border-blue-400/50 hover-glow' 
                    : 'bg-slate-700/50 text-slate-400 border border-slate-600 hover:bg-slate-700/70'
                }`}
              >
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                </svg>
              </button>
              <button
                onClick={() => handleViewModeChange('list')}
                className={`p-3 rounded-xl transition-all duration-300 ${
                  viewMode === 'list' 
                    ? 'bg-blue-600/30 text-blue-300 border border-blue-400/50 hover-glow' 
                    : 'bg-slate-700/50 text-slate-400 border border-slate-600 hover:bg-slate-700/70'
                }`}
              >
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
                </svg>
              </button>
            </div>

            {/* Enhanced Sort Dropdown */}
            <select
              value={sortBy}
              onChange={(e) => handleSortChange(e.target.value)}
              className="input bg-slate-800/50 border-slate-600 text-slate-200 focus:border-blue-400 focus:bg-slate-800/70"
            >
              <option value="featured">Featured</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
              <option value="rating">Rating</option>
              <option value="reviews">Most Reviews</option>
            </select>

            {/* Enhanced Filter Toggle */}
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="btn-outline hover-glow"
            >
              {showFilters ? 'Hide' : 'Show'} Filters
            </button>

            {/* Enhanced Analytics Button */}
            <button
              onClick={() => setShowReport(true)}
              className="btn-outline hover-glow"
            >
              📊 Analytics
            </button>
          </div>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Enhanced Filters Sidebar */}
          {showFilters && (
            <div className="lg:w-80">
              <div className="glass rounded-2xl p-6 sticky top-4 animate-slide-up">
                <h3 className="text-2xl font-bold gradient-text mb-6">Filters</h3>
                
                {/* Enhanced Categories */}
                <div className="mb-8">
                  <h4 className="text-lg font-semibold text-slate-200 mb-4">Categories</h4>
                  <div className="space-y-3">
                  {categories.map((category) => (
                      <label key={category} className="flex items-center cursor-pointer group">
                      <input
                        type="radio"
                        name="category"
                        value={category}
                        checked={selectedCategory === category}
                          onChange={(e) => handleCategoryChange(e.target.value)}
                          className="text-blue-600 focus:ring-blue-500 bg-slate-700 border-slate-600"
                      />
                        <span className="ml-3 text-slate-300 group-hover:text-white transition-colors">{category}</span>
                    </label>
                  ))}
                </div>
              </div>

                {/* Enhanced Price Range */}
                <div className="mb-8">
                  <h4 className="text-lg font-semibold text-slate-200 mb-4">Price Range</h4>
                  <div className="space-y-4">
                    <input
                      type="range"
                      min="0"
                      max="3000"
                      value={priceRange[1]}
                      onChange={(e) => setPriceRange([priceRange[0], parseInt(e.target.value)])}
                      className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer slider"
                    />
                    <div className="flex justify-between text-sm text-slate-400">
                      <span>${priceRange[0]}</span>
                      <span>${priceRange[1]}</span>
                    </div>
                  </div>
                </div>

                {/* Enhanced Clear Filters */}
                <button
                  onClick={() => {
                    setSelectedCategory("All")
                    setSearchQuery("")
                    setPriceRange([0, 3000])
                  }}
                  className="btn-outline w-full hover-glow"
                >
                  Clear Filters
                </button>
              </div>
            </div>
          )}

          {/* Enhanced Main Content */}
          <div className="flex-1">
            {/* Enhanced Toolbar */}
            <div className="glass rounded-2xl p-6 mb-8 animate-fade-in">
              <div className="flex justify-between items-center">
                <span className="text-slate-300 text-lg">
                  {pagination.total} products found
                  {pagination.pages > 1 && ` (Page ${page} of ${pagination.pages})`}
                </span>
                <div className="flex items-center space-x-4 text-sm text-slate-400">
                  <span>View: {viewMode}</span>
                  <span>•</span>
                  <span>Sort: {sortBy}</span>
                </div>
              </div>
            </div>

            {/* Enhanced Loading State */}
            {loading && (
              <div className="text-center py-16">
                <div className="spinner mx-auto mb-6"></div>
                <p className="text-slate-300 text-lg">Loading AI-powered products...</p>
                <div className="mt-4 flex justify-center space-x-2">
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-pink-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
              </div>
            )}

            {/* Enhanced Products Grid */}
            {!loading && (
              <div className={viewMode === 'grid' 
                ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
                : "space-y-6"
              }>
                {products.map((product, index) => (
                  <div 
                    key={product.id} 
                    className={`product-card card-hover group animate-fade-in`}
                    style={{animationDelay: `${index * 0.1}s`}}
                  >
                    <div className={`relative overflow-hidden ${viewMode === 'list' ? 'w-48 h-32' : ''}`}>
                      <img
                        src={product.images[0]}
                      alt={product.name}
                        className={`product-image object-cover ${viewMode === 'list' ? 'w-full h-full' : 'w-full h-64'}`}
                        onClick={() => handleProductClick(product)}
                      />
                      {product.original_price > product.price && (
                        <div className="absolute top-3 left-3 badge-success pulse-glow">
                          {Math.round(((product.original_price - product.price) / product.original_price) * 100)}% OFF
                        </div>
                      )}
                      <div className="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-all duration-300 flex space-x-2">
                        <button 
                          onClick={() => handleQuickView(product)}
                          className="btn-outline btn-sm hover-glow"
                          title="Quick View"
                        >
                          👁️
                        </button>
                        <button 
                          onClick={() => handleWishlist(product)}
                          className="btn-outline btn-sm hover-glow"
                          title="Add to Wishlist"
                        >
                          ❤️
                        </button>
                      </div>
                      <div className="absolute bottom-3 right-3 opacity-0 group-hover:opacity-100 transition-all duration-300">
                        {isAuthenticated ? (
                          hasPremiumAccess() ? (
                            <button 
                              onClick={() => handleAddToCart(product)}
                              className="btn-primary btn-sm hover-glow"
                              title="Add to Cart"
                            >
                              🛒 Add to Cart
                            </button>
                          ) : (
                            <button 
                              onClick={() => {
                                toast.error('Premium membership required to use the cart')
                                navigate('/account?tab=premium')
                              }}
                              className="btn-outline btn-sm bg-yellow-600/20 border-yellow-400/50 text-yellow-300 hover-glow"
                              title="Premium Required"
                            >
                              ⭐ Premium Required
                            </button>
                          )
                        ) : (
                          <button 
                            onClick={() => {
                              toast.error('Please sign in to add items to cart')
                              navigate('/login')
                            }}
                            className="btn-outline btn-sm bg-blue-600/20 border-blue-400/50 text-blue-300 hover-glow"
                            title="Sign In Required"
                          >
                            🔐 Sign In Required
                          </button>
                        )}
                      </div>
                    </div>
                    <div className={`p-6 ${viewMode === 'list' ? 'flex-1' : ''}`}>
                      <div className="flex items-center justify-between mb-3">
                        <span className="badge-primary hover-glow">{product.category}</span>
                      <div className="rating">
                          <span className="star text-xl">★</span>
                          <span className="text-sm text-slate-400 ml-2">
                          {product.rating} ({product.reviews})
                        </span>
                      </div>
                    </div>
                      <h3 
                        className="text-xl font-bold text-slate-200 mb-3 group-hover:text-blue-300 transition-colors cursor-pointer hover-lift"
                        onClick={() => handleProductClick(product)}
                      >
                      {product.name}
                    </h3>
                      <div className="flex items-center space-x-3 mb-4">
                        <span className="price text-2xl">${product.price}</span>
                        {product.original_price > product.price && (
                          <span className="price-original text-lg">${product.original_price}</span>
                        )}
                      </div>
                      {viewMode === 'list' && (
                        <div className="flex space-x-3">
                          {isAuthenticated ? (
                            hasPremiumAccess() ? (
                              <button 
                                onClick={() => handleAddToCart(product)}
                                className="btn-primary btn-sm hover-glow"
                                title="Add to Cart"
                              >
                                🛒 Add to Cart
                              </button>
                            ) : (
                              <button 
                                onClick={() => {
                                  toast.error('Premium membership required to use the cart')
                                  navigate('/account?tab=premium')
                                }}
                                className="btn-outline btn-sm bg-yellow-600/20 border-yellow-400/50 text-yellow-300 hover-glow"
                                title="Premium Required"
                              >
                                ⭐ Premium Required
                              </button>
                            )
                          ) : (
                            <button 
                              onClick={() => {
                                toast.error('Please sign in to add items to cart')
                                navigate('/login')
                              }}
                              className="btn-outline btn-sm bg-blue-600/20 border-blue-400/50 text-blue-300 hover-glow"
                              title="Sign In Required"
                            >
                              🔐 Sign In Required
                            </button>
                          )}
                          <button 
                            onClick={() => handleQuickView(product)}
                            className="btn-outline btn-sm hover-glow"
                          >
                            👁️ Quick View
                          </button>
                        </div>
                      )}
                  </div>
                </div>
              ))}
            </div>
            )}

            {/* Enhanced Pagination */}
            {pagination.pages > 1 && (
              <div className="flex justify-center items-center space-x-3 mt-12">
                <button
                  onClick={() => setPage(Math.max(1, page - 1))}
                  disabled={page === 1}
                  className="btn-outline btn-sm disabled:opacity-50 hover-glow"
                >
                  Previous
                </button>
                {Array.from({ length: pagination.pages }, (_, i) => i + 1).map((pageNum) => (
                  <button
                    key={pageNum}
                    onClick={() => setPage(pageNum)}
                    className={`btn-sm hover-glow ${
                      page === pageNum 
                        ? 'btn-primary pulse-glow' 
                        : 'btn-outline'
                    }`}
                  >
                    {pageNum}
                  </button>
                ))}
                <button
                  onClick={() => setPage(Math.min(pagination.pages, page + 1))}
                  disabled={page === pagination.pages}
                  className="btn-outline btn-sm disabled:opacity-50 hover-glow"
                >
                  Next
                </button>
              </div>
            )}

            {/* Enhanced Empty State */}
            {!loading && products.length === 0 && (
              <div className="text-center py-16">
                <div className="text-8xl mb-6 floating">🔍</div>
                <h3 className="text-3xl font-bold gradient-text mb-4">No products found</h3>
                <p className="text-slate-400 text-lg mb-8">Try adjusting your filters or search terms</p>
                <div className="flex justify-center space-x-4">
                  <button
                    onClick={() => {
                      setSelectedCategory("All")
                      setSearchQuery("")
                      setPriceRange([0, 3000])
                    }}
                    className="btn-primary hover-glow"
                  >
                    Clear Filters
                  </button>
                  <button
                    onClick={() => setShowFeedback(true)}
                    className="btn-outline hover-glow"
                  >
                    Report Issue
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Enhanced Quick View Modal */}
      {selectedProduct && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fade-in">
          <div className="glass rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto animate-scale-in">
            <div className="p-8">
              <div className="flex justify-between items-start mb-6">
                <h2 className="text-3xl font-bold gradient-text">{selectedProduct.name}</h2>
                <button
                  onClick={() => setSelectedProduct(null)}
                  className="btn-outline btn-sm hover-glow"
                >
                  ✕
                </button>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="relative">
                  <img
                    src={selectedProduct.images[0]}
                    alt={selectedProduct.name}
                    className="w-full h-96 object-cover rounded-xl"
                  />
                  {selectedProduct.original_price > selectedProduct.price && (
                    <div className="absolute top-4 left-4 badge-success pulse-glow">
                      {Math.round(((selectedProduct.original_price - selectedProduct.price) / selectedProduct.original_price) * 100)}% OFF
                    </div>
                  )}
                </div>
                
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span className="badge-primary">{selectedProduct.category}</span>
                    <div className="rating">
                      <span className="star text-2xl">★</span>
                      <span className="text-lg text-slate-400 ml-2">
                        {selectedProduct.rating} ({selectedProduct.reviews} reviews)
                      </span>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4 mb-6">
                    <span className="price text-3xl">${selectedProduct.price}</span>
                    {selectedProduct.original_price > selectedProduct.price && (
                      <span className="price-original text-xl">${selectedProduct.original_price}</span>
                    )}
                  </div>
                  
                  <p className="text-slate-300 text-lg mb-6 leading-relaxed">
                    {selectedProduct.description}
                  </p>
                  
                  <div className="space-y-4">
                    {isAuthenticated ? (
                      hasPremiumAccess() ? (
                        <button 
                          onClick={() => {
                            handleAddToCart(selectedProduct)
                            setSelectedProduct(null)
                          }}
                          className="btn-primary w-full hover-glow"
                        >
                          🛒 Add to Cart
                        </button>
                      ) : (
                        <button 
                          onClick={() => {
                            toast.error('Premium membership required to use the cart')
                            navigate('/account?tab=premium')
                          }}
                          className="btn-outline w-full bg-yellow-600/20 border-yellow-400/50 text-yellow-300 hover-glow"
                        >
                          ⭐ Premium Required
                        </button>
                      )
                    ) : (
                      <button 
                        onClick={() => {
                          toast.error('Please sign in to add items to cart')
                          navigate('/login')
                        }}
                        className="btn-outline w-full bg-blue-600/20 border-blue-400/50 text-blue-300 hover-glow"
                      >
                        🔐 Sign In Required
                      </button>
                    )}
                    
                    <button 
                      onClick={() => handleWishlist(selectedProduct)}
                      className="btn-outline w-full hover-glow"
                    >
                      ❤️ Add to Wishlist
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Analytics Modal */}
      {showReport && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="glass rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-8">
              <div className="flex justify-between items-start mb-6">
                <h2 className="text-3xl font-bold gradient-text">Analytics Report</h2>
                <button
                  onClick={() => setShowReport(false)}
                  className="btn-outline btn-sm hover-glow"
                >
                  ✕
                </button>
              </div>
              
              <div className="space-y-6">
                <div className="grid grid-cols-2 gap-4">
                  <div className="glass rounded-xl p-4 text-center">
                    <div className="text-2xl font-bold text-blue-400">{analytics.pageViews}</div>
                    <div className="text-slate-400">Page Views</div>
                  </div>
                  <div className="glass rounded-xl p-4 text-center">
                    <div className="text-2xl font-bold text-green-400">{analytics.productClicks}</div>
                    <div className="text-slate-400">Product Clicks</div>
                  </div>
                  <div className="glass rounded-xl p-4 text-center">
                    <div className="text-2xl font-bold text-purple-400">{analytics.cartAdds}</div>
                    <div className="text-slate-400">Cart Adds</div>
                  </div>
                  <div className="glass rounded-xl p-4 text-center">
                    <div className="text-2xl font-bold text-pink-400">{analytics.filterUses}</div>
                    <div className="text-slate-400">Filter Uses</div>
                  </div>
                </div>
                
                <div className="glass rounded-xl p-6">
                  <h3 className="text-xl font-semibold text-slate-200 mb-4">Current Filters</h3>
                  <div className="space-y-2 text-slate-300">
                    <div>Category: {selectedCategory}</div>
                    <div>Sort: {sortBy}</div>
                    <div>Price Range: ${priceRange[0]} - ${priceRange[1]}</div>
                    <div>Search: {searchQuery || 'None'}</div>
                  </div>
                </div>
                
                <div className="glass rounded-xl p-6">
                  <h3 className="text-xl font-semibold text-slate-200 mb-4">Top Products</h3>
                  <div className="space-y-2">
                    {products
                      .sort((a, b) => b.rating - a.rating)
                      .slice(0, 5)
                      .map((product, index) => (
                        <div key={product.id} className="flex justify-between items-center text-slate-300">
                          <span>{index + 1}. {product.name}</span>
                          <span className="text-yellow-400">★ {product.rating}</span>
                        </div>
                      ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Feedback Modal */}
      {showFeedback && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-lg w-full">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-xl font-bold">Send Feedback</h2>
                <button
                  onClick={() => setShowFeedback(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
              <form className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Feedback Type
                  </label>
                  <select className="input w-full">
                    <option>General Feedback</option>
                    <option>Bug Report</option>
                    <option>Feature Request</option>
                    <option>Product Suggestion</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Subject
                  </label>
                  <input
                    type="text"
                    placeholder="Brief description"
                    className="input w-full"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Message
                  </label>
                  <textarea
                    rows={4}
                    placeholder="Tell us more..."
                    className="input w-full"
                  />
                </div>
                <div className="flex space-x-2">
                  <button
                    type="button"
                    onClick={() => setShowFeedback(false)}
                    className="btn-outline flex-1"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    onClick={(e) => {
                      e.preventDefault()
                      toast.success('Feedback sent successfully!')
                      setShowFeedback(false)
                      trackEvent('feedback_submitted', { timestamp: new Date().toISOString() })
                    }}
                    className="btn-primary flex-1"
                  >
                    Send Feedback
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ProductsPage 