import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Sparkles, 
  ShoppingBag, 
  Star, 
  ArrowRight,
  Bot,
  Zap,
  Target,
  TrendingUp
} from 'lucide-react';
import axios from 'axios';

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

const HomePage: React.FC = () => {
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchFeaturedProducts();
  }, []);

  const fetchFeaturedProducts = async () => {
    try {
      const response = await axios.get('/api/v1/products/?featured=true&limit=6');
      setFeaturedProducts(response.data.items || []);
    } catch (error) {
      console.error('Failed to fetch featured products:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const features = [
    {
      icon: <Bot className="w-8 h-8" />,
      title: "AI-Powered Recommendations",
      description: "Get personalized product suggestions based on your preferences and behavior."
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Smart Search",
      description: "Find exactly what you're looking for with our intelligent search technology."
    },
    {
      icon: <Target className="w-8 h-8" />,
      title: "Precision Matching",
      description: "Our AI analyzes your needs to match you with the perfect products."
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: "Trending Insights",
      description: "Stay ahead with real-time trending products and market insights."
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 px-4 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-600/20 to-secondary-700/20"></div>
        <div className="relative container mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="flex items-center justify-center mb-6">
              <Sparkles className="w-8 h-8 text-yellow-400 mr-2" />
              <span className="text-yellow-400 font-semibold">AI-Powered Shopping</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
              Discover Your Perfect
              <span className="text-gradient block">Products</span>
            </h1>
            
            <p className="text-xl text-white/80 mb-8 max-w-2xl mx-auto">
              Experience the future of shopping with AI-powered recommendations, 
              intelligent search, and personalized product discovery.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/products" className="btn btn-primary text-lg px-8 py-4">
                <ShoppingBag className="w-5 h-5 mr-2" />
                Start Shopping
              </Link>
              <Link to="/register" className="btn btn-secondary text-lg px-8 py-4">
                Join for Free
                <ArrowRight className="w-5 h-5 ml-2" />
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-white mb-4">
              Why Choose <span className="text-gradient">ShopEase AI</span>?
            </h2>
            <p className="text-xl text-white/70 max-w-3xl mx-auto">
              Our cutting-edge AI technology revolutionizes your shopping experience 
              with intelligent features designed to save you time and money.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="card text-center group hover:scale-105 transition-transform"
              >
                <div className="text-gradient mb-4 group-hover:scale-110 transition-transform">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">
                  {feature.title}
                </h3>
                <p className="text-white/70">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold text-white mb-4">
              Featured <span className="text-gradient">Products</span>
            </h2>
            <p className="text-xl text-white/70 max-w-3xl mx-auto">
              Discover our handpicked selection of premium products, 
              carefully curated by our AI for the best shopping experience.
            </p>
          </motion.div>

          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[...Array(6)].map((_, index) => (
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
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {featuredProducts.map((product, index) => (
                <motion.div
                  key={product.id}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="card group hover:scale-105 transition-transform"
                >
                  <div className="relative mb-4">
                    <img
                      src={product.image_url || `https://picsum.photos/400/300?random=${product.id}`}
                      alt={product.name}
                      className="w-full h-48 object-cover rounded-lg"
                    />
                    {product.ai_score && (
                      <div className="absolute top-2 right-2 bg-gradient-to-r from-primary-500 to-secondary-500 text-white px-2 py-1 rounded-full text-xs font-semibold flex items-center">
                        <Star className="w-3 h-3 mr-1" />
                        AI Score: {product.ai_score}
                      </div>
                    )}
                    {product.sale_price && (
                      <div className="absolute top-2 left-2 bg-red-500 text-white px-2 py-1 rounded-full text-xs font-semibold">
                        SALE
                      </div>
                    )}
                  </div>
                  
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
                  
                  <Link
                    to={`/products/${product.id}`}
                    className="btn btn-primary w-full text-center"
                  >
                    View Details
                  </Link>
                </motion.div>
              ))}
            </div>
          )}

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            viewport={{ once: true }}
            className="text-center mt-12"
          >
            <Link to="/products" className="btn btn-secondary text-lg px-8 py-4">
              View All Products
              <ArrowRight className="w-5 h-5 ml-2" />
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default HomePage; 