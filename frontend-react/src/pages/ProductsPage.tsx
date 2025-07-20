import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Search, 
  Filter, 
  Grid, 
  List,
  Star,
  ShoppingCart,
  Eye
} from 'lucide-react';
import axios from 'axios';
import { useCart } from '../contexts/CartContext';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  sale_price?: number;
  image_url: string;
  category: string;
  stock_quantity: number;
  is_featured: boolean;
  ai_score?: number;
}

const ProductsPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [searchQuery, setSearchQuery] = useState(searchParams.get('search') || '');
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get('category') || '');
  const [priceRange, setPriceRange] = useState(searchParams.get('price') || '');
  const { addToCart } = useCart();

  useEffect(() => {
    fetchProducts();
  }, [searchQuery, selectedCategory, priceRange]);

  const fetchProducts = async () => {
    try {
      setIsLoading(true);
      const params = new URLSearchParams();
      if (searchQuery) params.append('search', searchQuery);
      if (selectedCategory) params.append('category', selectedCategory);
      if (priceRange) params.append('price_range', priceRange);
      
      const response = await axios.get(`/api/v1/products/?${params.toString()}`);
      setProducts(response.data.items || []);
    } catch (error) {
      console.error('Failed to fetch products:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const newParams = new URLSearchParams();
    if (searchQuery) newParams.set('search', searchQuery);
    if (selectedCategory) newParams.set('category', selectedCategory);
    if (priceRange) newParams.set('price', priceRange);
    setSearchParams(newParams);
  };

  const handleAddToCart = async (productId: number) => {
    try {
      await addToCart(productId, 1);
    } catch (error) {
      console.error('Failed to add to cart:', error);
    }
  };

  const categories = [
    'Electronics',
    'Clothing',
    'Home & Garden',
    'Sports',
    'Books',
    'Beauty',
    'Toys',
    'Automotive'
  ];

  const priceRanges = [
    { label: 'All Prices', value: '' },
    { label: 'Under $50', value: '0-50' },
    { label: '$50 - $100', value: '50-100' },
    { label: '$100 - $200', value: '100-200' },
    { label: '$200 - $500', value: '200-500' },
    { label: 'Over $500', value: '500-' }
  ];

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="container mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-white mb-4">
            Discover <span className="text-gradient">Products</span>
          </h1>
          <p className="text-xl text-white/70 max-w-3xl mx-auto">
            Explore our vast collection of products, carefully curated and enhanced with AI-powered recommendations.
          </p>
        </motion.div>

        {/* Filters and Search */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="card mb-8"
        >
          <form onSubmit={handleSearch} className="space-y-6">
            {/* Search Bar */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/60" />
              <input
                type="text"
                placeholder="Search products..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-primary-400"
              />
            </div>

            {/* Filters */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Category Filter */}
              <div>
                <label className="block text-white font-semibold mb-2">Category</label>
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-400"
                >
                  <option value="">All Categories</option>
                  {categories.map((category) => (
                    <option key={category} value={category}>{category}</option>
                  ))}
                </select>
              </div>

              {/* Price Range Filter */}
              <div>
                <label className="block text-white font-semibold mb-2">Price Range</label>
                <select
                  value={priceRange}
                  onChange={(e) => setPriceRange(e.target.value)}
                  className="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-primary-400"
                >
                  {priceRanges.map((range) => (
                    <option key={range.value} value={range.value}>{range.label}</option>
                  ))}
                </select>
              </div>

              {/* View Mode */}
              <div>
                <label className="block text-white font-semibold mb-2">View Mode</label>
                <div className="flex space-x-2">
                  <button
                    type="button"
                    onClick={() => setViewMode('grid')}
                    className={`flex-1 px-4 py-3 rounded-lg border transition-colors ${
                      viewMode === 'grid'
                        ? 'bg-primary-500 border-primary-500 text-white'
                        : 'bg-white/10 border-white/20 text-white hover:bg-white/20'
                    }`}
                  >
                    <Grid className="w-5 h-5 mx-auto" />
                  </button>
                  <button
                    type="button"
                    onClick={() => setViewMode('list')}
                    className={`flex-1 px-4 py-3 rounded-lg border transition-colors ${
                      viewMode === 'list'
                        ? 'bg-primary-500 border-primary-500 text-white'
                        : 'bg-white/10 border-white/20 text-white hover:bg-white/20'
                    }`}
                  >
                    <List className="w-5 h-5 mx-auto" />
                  </button>
                </div>
              </div>
            </div>

            <button type="submit" className="btn btn-primary w-full md:w-auto">
              <Filter className="w-5 h-5 mr-2" />
              Apply Filters
            </button>
          </form>
        </motion.div>

        {/* Products Grid */}
        {isLoading ? (
          <div className={`grid gap-6 ${
            viewMode === 'grid' 
              ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4' 
              : 'grid-cols-1'
          }`}>
            {[...Array(8)].map((_, index) => (
              <div key={index} className="card animate-pulse">
                <div className="bg-white/10 h-48 rounded-lg mb-4"></div>
                <div className="space-y-2">
                  <div className="bg-white/10 h-4 rounded"></div>
                  <div className="bg-white/10 h-4 rounded w-3/4"></div>
                  <div className="bg-white/10 h-6 rounded w-1/2"></div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className={`grid gap-6 ${
            viewMode === 'grid' 
              ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4' 
              : 'grid-cols-1'
          }`}>
            {products.map((product, index) => (
              <motion.div
                key={product.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.05 }}
                className={`card group hover:scale-105 transition-transform ${
                  viewMode === 'list' ? 'flex' : ''
                }`}
              >
                <div className={`relative ${viewMode === 'list' ? 'w-48 flex-shrink-0' : 'mb-4'}`}>
                  <img
                    src={product.image_url || `https://picsum.photos/400/300?random=${product.id}`}
                    alt={product.name}
                    className={`object-cover rounded-lg ${
                      viewMode === 'list' ? 'w-full h-32' : 'w-full h-48'
                    }`}
                  />
                  {product.ai_score && (
                    <div className="absolute top-2 right-2 bg-gradient-to-r from-primary-500 to-secondary-500 text-white px-2 py-1 rounded-full text-xs font-semibold flex items-center">
                      <Star className="w-3 h-3 mr-1" />
                      {product.ai_score}
                    </div>
                  )}
                  {product.sale_price && (
                    <div className="absolute top-2 left-2 bg-red-500 text-white px-2 py-1 rounded-full text-xs font-semibold">
                      SALE
                    </div>
                  )}
                </div>
                
                <div className={`flex-1 ${viewMode === 'list' ? 'ml-4' : ''}`}>
                  <h3 className="text-lg font-semibold text-white mb-2 group-hover:text-gradient transition-colors">
                    {product.name}
                  </h3>
                  
                  <p className="text-white/70 text-sm mb-4 line-clamp-2">
                    {product.description}
                  </p>
                  
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-2">
                      {product.sale_price ? (
                        <>
                          <span className="text-lg font-bold text-white">
                            ${product.sale_price}
                          </span>
                          <span className="text-white/60 line-through">
                            ${product.price}
                          </span>
                        </>
                      ) : (
                        <span className="text-lg font-bold text-white">
                          ${product.price}
                        </span>
                      )}
                    </div>
                    <span className="text-white/60 text-sm">
                      {product.stock_quantity > 0 ? 'In Stock' : 'Out of Stock'}
                    </span>
                  </div>
                  
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleAddToCart(product.id)}
                      disabled={product.stock_quantity <= 0}
                      className="flex-1 btn btn-primary text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <ShoppingCart className="w-4 h-4 mr-1" />
                      Add to Cart
                    </button>
                    <button className="btn btn-secondary text-sm">
                      <Eye className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}

        {/* No Products Message */}
        {!isLoading && products.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <div className="text-white/60 text-lg">
              No products found matching your criteria.
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default ProductsPage; 