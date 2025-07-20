import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useCart } from '../components/ui/CartProvider'

// Mock data for demonstration with real product images
const featuredProducts = [
  {
    id: 1,
    name: "iPhone 15 Pro",
    price: 999.99,
    originalPrice: 1199.99,
    image: "https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400&h=400&fit=crop&crop=center",
    rating: 4.8,
    reviews: 1250,
    category: "Electronics"
  },
  {
    id: 2,
    name: "MacBook Pro 16\"",
    price: 2499.99,
    originalPrice: 2799.99,
    image: "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop&crop=center",
    rating: 4.9,
    reviews: 890,
    category: "Electronics"
  },
  {
    id: 3,
    name: "Sony WH-1000XM5",
    price: 349.99,
    originalPrice: 399.99,
    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop&crop=center",
    rating: 4.7,
    reviews: 2100,
    category: "Electronics"
  },
  {
    id: 4,
    name: "Apple Watch Series 9",
    price: 399.99,
    originalPrice: 449.99,
    image: "https://images.unsplash.com/photo-1544117519-31a4b719223d?w=400&h=400&fit=crop&crop=center",
    rating: 4.6,
    reviews: 750,
    category: "Wearables"
  }
]

const categories = [
  { id: 1, name: "Electronics", icon: "📱", count: 15 },
  { id: 2, name: "Fashion", icon: "👕", count: 23 },
  { id: 3, name: "Home & Garden", icon: "🏠", count: 12 },
  { id: 4, name: "Sports", icon: "⚽", count: 8 },
  { id: 5, name: "Books", icon: "📚", count: 45 },
  { id: 6, name: "Toys", icon: "🎮", count: 19 }
]

const HomePage = () => {
  const [currentSlide, setCurrentSlide] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const { addItem } = useCart()

  useEffect(() => {
    // Simulate loading
    const timer = setTimeout(() => setIsLoading(false), 1000)
    return () => clearTimeout(timer)
  }, [])

  useEffect(() => {
    // Auto-slide banner
    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % 3)
    }, 5000)
    return () => clearInterval(interval)
  }, [])

  const banners = [
    {
      title: "AI-Powered Recommendations",
      subtitle: "Discover products tailored just for you",
      image: "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=1200&h=400&fit=crop&crop=center",
      cta: "Explore Now"
    },
    {
      title: "Modern Payment Methods",
      subtitle: "Pay with crypto, digital wallets, and more",
      image: "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=1200&h=400&fit=crop&crop=center",
      cta: "Learn More"
    },
    {
      title: "Fast & Secure Shopping",
      subtitle: "Shop with confidence on our secure platform",
      image: "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=1200&h=400&fit=crop&crop=center",
      cta: "Start Shopping"
    }
  ]

  const handleAddToCart = (product: any) => {
    addItem({
      id: product.id,
      name: product.name,
      price: product.price,
      originalPrice: product.originalPrice,
      image: product.image,
      category: product.category
    })
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {/* Hero Banner */}
      <section className="relative h-96 overflow-hidden">
        <div className="relative h-full">
          {banners.map((banner, index) => (
            <div
              key={index}
              className={`absolute inset-0 transition-opacity duration-1000 ${
                index === currentSlide ? 'opacity-100' : 'opacity-0'
              }`}
            >
              <div className="absolute inset-0 bg-gradient-to-r from-black/70 to-transparent z-10"></div>
              <img
                src={banner.image}
                alt={banner.title}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 flex items-center z-20">
                <div className="container mx-auto px-4">
                  <div className="max-w-2xl text-white">
                    <h1 className="text-5xl font-bold mb-4 animate-fade-in text-shadow-lg">
                      {banner.title}
                    </h1>
                    <p className="text-xl mb-8 animate-slide-up text-gray-200">
                      {banner.subtitle}
                    </p>
                    <button className="btn-primary text-lg px-8 py-3 animate-scale-in hover-glow">
                      {banner.cta}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
          
          {/* Banner Navigation */}
          <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 z-30 flex space-x-2">
            {banners.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentSlide(index)}
                className={`w-3 h-3 rounded-full transition-colors ${
                  index === currentSlide ? 'bg-white' : 'bg-white/50'
                }`}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="py-16 bg-gray-800">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 gradient-text">
            Shop by Category
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {categories.map((category) => (
              <Link
                key={category.id}
                to={`/products?category=${category.name}`}
                className="group text-center p-6 rounded-xl bg-gray-700 hover:bg-gray-600 transition-all duration-300 hover:shadow-lg hover-lift"
              >
                <div className="text-4xl mb-3 group-hover:scale-110 transition-transform duration-300">
                  {category.icon}
                </div>
                <h3 className="font-semibold text-white mb-1">
                  {category.name}
                </h3>
                <p className="text-sm text-gray-400">
                  {category.count} items
                </p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-16 bg-gray-900">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 gradient-text">
            Featured Products
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {featuredProducts.map((product) => (
              <div key={product.id} className="product-card group">
                <div className="relative overflow-hidden">
                  <img
                    src={product.image}
                    alt={product.name}
                    className="product-image w-full h-64 object-cover"
                  />
                  {product.originalPrice > product.price && (
                    <div className="absolute top-2 left-2 badge-success">
                      {Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100)}% OFF
                    </div>
                  )}
                  <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <button 
                      onClick={() => handleAddToCart(product)}
                      className="btn-primary btn-sm"
                    >
                      Add to Cart
                    </button>
                  </div>
                </div>
                <div className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="badge-primary">{product.category}</span>
                    <div className="rating">
                      <span className="star">★</span>
                      <span className="text-sm text-gray-400 ml-1">
                        {product.rating} ({product.reviews})
                      </span>
                    </div>
                  </div>
                  <h3 className="font-semibold text-white mb-2 group-hover:text-blue-400 transition-colors">
                    {product.name}
                  </h3>
                  <div className="flex items-center space-x-2">
                    <span className="price">${product.price}</span>
                    {product.originalPrice > product.price && (
                      <span className="price-original">${product.originalPrice}</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div className="text-center mt-12">
            <Link to="/products" className="btn-primary text-lg px-8 py-3">
              View All Products
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 bg-gray-800">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 gradient-text">
            Why Choose Us
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🤖</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-white">AI Recommendations</h3>
              <p className="text-gray-400">
                Get personalized product suggestions based on your preferences and behavior.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">💳</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-white">Modern Payments</h3>
              <p className="text-gray-400">
                Pay with cryptocurrency, digital wallets, and traditional methods.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-yellow-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🚀</span>
              </div>
              <h3 className="text-xl font-semibold mb-3 text-white">Fast Delivery</h3>
              <p className="text-gray-400">
                Quick and reliable shipping to get your products to you faster.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Newsletter */}
      <section className="py-16 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">
            Stay Updated
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Get the latest products and exclusive offers delivered to your inbox.
          </p>
          <div className="max-w-md mx-auto flex">
            <input
              type="email"
              placeholder="Enter your email"
              className="flex-1 px-4 py-3 rounded-l-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-white"
            />
            <button className="btn-primary rounded-l-none">
              Subscribe
            </button>
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage 