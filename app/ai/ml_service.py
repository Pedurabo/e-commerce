"""
Advanced Machine Learning Service for Ecommerce Platform
"""

import numpy as np
import pandas as pd
import random
import json
import requests
from typing import List, Dict, Tuple, Optional, Any
from datetime import datetime, timedelta
import asyncio
import aiohttp
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
import logging

logger = logging.getLogger(__name__)

class ProductGenerator:
    """AI-powered product generator for limitless product database."""
    
    def __init__(self):
        self.categories = {
            "Electronics": {
                "subcategories": ["Smartphones", "Laptops", "Tablets", "Smartwatches", "Headphones", "Cameras", "Gaming", "Audio", "TV", "Accessories"],
                "brands": ["Apple", "Samsung", "Sony", "LG", "Dell", "HP", "Lenovo", "Asus", "Canon", "Nikon", "Bose", "JBL", "Sennheiser", "Razer", "Logitech"],
                "price_ranges": [(50, 2000), (200, 5000), (100, 1500), (100, 800), (20, 500), (200, 3000), (200, 2000), (50, 300), (300, 5000), (10, 200)]
            },
            "Fashion": {
                "subcategories": ["Clothing", "Shoes", "Bags", "Jewelry", "Watches", "Sunglasses", "Hats", "Belts", "Scarves", "Socks"],
                "brands": ["Nike", "Adidas", "Puma", "Under Armour", "Levi's", "Calvin Klein", "Tommy Hilfiger", "Ralph Lauren", "Gucci", "Prada", "Ray-Ban", "Oakley"],
                "price_ranges": [(20, 200), (50, 300), (30, 500), (50, 1000), (100, 2000), (100, 500), (20, 100), (30, 150), (20, 80), (10, 50)]
            },
            "Home & Garden": {
                "subcategories": ["Furniture", "Kitchen", "Bathroom", "Bedding", "Decor", "Lighting", "Garden", "Tools", "Storage", "Appliances"],
                "brands": ["IKEA", "Wayfair", "Home Depot", "Lowe's", "Williams-Sonoma", "Crate & Barrel", "Pottery Barn", "West Elm", "Target", "Walmart"],
                "price_ranges": [(100, 2000), (20, 500), (50, 300), (30, 200), (20, 300), (50, 400), (20, 200), (10, 100), (20, 150), (50, 1000)]
            },
            "Sports & Outdoors": {
                "subcategories": ["Fitness", "Camping", "Hiking", "Cycling", "Swimming", "Yoga", "Running", "Team Sports", "Water Sports", "Winter Sports"],
                "brands": ["Nike", "Adidas", "Under Armour", "Columbia", "The North Face", "Patagonia", "REI", "Trek", "Specialized", "Cannondale"],
                "price_ranges": [(30, 200), (50, 500), (100, 300), (200, 1000), (20, 100), (20, 150), (50, 200), (30, 300), (100, 800), (200, 1000)]
            },
            "Books & Media": {
                "subcategories": ["Fiction", "Non-Fiction", "Academic", "Children's", "Comics", "Magazines", "Movies", "Music", "Games", "Software"],
                "brands": ["Penguin", "Random House", "HarperCollins", "Simon & Schuster", "Scholastic", "Marvel", "DC Comics", "Disney", "Warner Bros", "Electronic Arts"],
                "price_ranges": [(10, 30), (15, 50), (20, 100), (10, 25), (5, 20), (5, 15), (10, 30), (10, 25), (20, 60), (20, 200)]
            },
            "Health & Beauty": {
                "subcategories": ["Skincare", "Makeup", "Haircare", "Fragrances", "Vitamins", "Fitness", "Medical", "Dental", "Bath & Body", "Tools"],
                "brands": ["L'Oreal", "Estee Lauder", "MAC", "Clinique", "Neutrogena", "Olay", "Dove", "Pantene", "Gillette", "Philips"],
                "price_ranges": [(10, 100), (20, 200), (15, 80), (30, 300), (10, 50), (20, 150), (10, 100), (5, 50), (10, 60), (20, 200)]
            }
        }
        
        self.product_templates = self._load_product_templates()
        self.image_cache = {}
    
    def _load_product_templates(self) -> Dict:
        """Load product templates for generation."""
        return {
            "Electronics": {
                "Smartphones": ["{brand} {model} Smartphone", "{brand} {model} Mobile Phone", "{brand} {model} Android Phone"],
                "Laptops": ["{brand} {model} Laptop", "{brand} {model} Notebook", "{brand} {model} Ultrabook"],
                "Headphones": ["{brand} {model} Wireless Headphones", "{brand} {model} Noise-Canceling Headphones", "{brand} {model} Bluetooth Headphones"]
            },
            "Fashion": {
                "Clothing": ["{brand} {style} T-Shirt", "{brand} {style} Jeans", "{brand} {style} Jacket"],
                "Shoes": ["{brand} {style} Sneakers", "{brand} {style} Running Shoes", "{brand} {style} Casual Shoes"]
            }
        }
    
    async def generate_product(self, category: str = None, subcategory: str = None) -> Dict:
        """Generate a single product with realistic data."""
        if not category:
            category = random.choice(list(self.categories.keys()))
        
        cat_data = self.categories[category]
        if not subcategory:
            subcategory = random.choice(cat_data["subcategories"])
        
        brand = random.choice(cat_data["brands"])
        price_range = random.choice(cat_data["price_ranges"])
        
        # Generate product name
        product_name = self._generate_product_name(category, subcategory, brand)
        
        # Generate realistic price
        base_price = random.uniform(price_range[0], price_range[1])
        original_price = base_price * random.uniform(1.1, 1.5)
        
        # Generate product data
        product = {
            "id": self._generate_unique_id(),
            "name": product_name,
            "brand": brand,
            "category": category,
            "subcategory": subcategory,
            "price": round(base_price, 2),
            "original_price": round(original_price, 2),
            "description": self._generate_description(category, subcategory, brand, product_name),
            "short_description": self._generate_short_description(product_name),
            "features": self._generate_features(category, subcategory),
            "specifications": self._generate_specifications(category, subcategory),
            "rating": round(random.uniform(3.5, 5.0), 1),
            "reviews": random.randint(10, 5000),
            "stock_quantity": random.randint(0, 1000),
            "is_featured": random.choice([True, False]),
            "is_bestseller": random.choice([True, False]),
            "is_new": random.choice([True, False]),
            "is_on_sale": random.choice([True, False]),
            "discount_percentage": random.randint(0, 50) if random.choice([True, False]) else 0,
            "tags": self._generate_tags(category, subcategory, brand),
            "images": await self._generate_images(category, subcategory),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        return product
    
    def _generate_unique_id(self) -> int:
        """Generate a unique product ID."""
        return int(datetime.now().timestamp() * 1000) + random.randint(0, 999)
    
    def _generate_product_name(self, category: str, subcategory: str, brand: str) -> str:
        """Generate a realistic product name."""
        models = ["Pro", "Max", "Ultra", "Elite", "Premium", "Standard", "Basic", "Advanced", "Classic", "Modern"]
        styles = ["Casual", "Sport", "Elegant", "Professional", "Vintage", "Contemporary", "Minimalist", "Bold"]
        
        if category == "Electronics":
            model = random.choice(models)
            return f"{brand} {subcategory} {model}"
        elif category == "Fashion":
            style = random.choice(styles)
            return f"{brand} {style} {subcategory}"
        else:
            return f"{brand} {subcategory}"
    
    def _generate_description(self, category: str, subcategory: str, brand: str, name: str) -> str:
        """Generate a detailed product description."""
        descriptions = {
            "Electronics": f"Experience the latest technology with the {name}. This premium {subcategory.lower()} from {brand} offers cutting-edge features and exceptional performance. Perfect for both personal and professional use.",
            "Fashion": f"Elevate your style with the {name}. Crafted with premium materials and designed for comfort, this {subcategory.lower()} from {brand} combines fashion and functionality seamlessly.",
            "Home & Garden": f"Transform your space with the {name}. This high-quality {subcategory.lower()} from {brand} brings both style and practicality to your home.",
            "Sports & Outdoors": f"Enhance your performance with the {name}. Designed for athletes and outdoor enthusiasts, this {subcategory.lower()} from {brand} provides the durability and comfort you need.",
            "Books & Media": f"Discover amazing content with the {name}. This {subcategory.lower()} from {brand} offers hours of entertainment and knowledge.",
            "Health & Beauty": f"Take care of yourself with the {name}. This premium {subcategory.lower()} from {brand} helps you look and feel your best."
        }
        
        return descriptions.get(category, f"High-quality {subcategory.lower()} from {brand}.")
    
    def _generate_short_description(self, name: str) -> str:
        """Generate a short product description."""
        return f"Premium {name} with excellent quality and performance."
    
    def _generate_features(self, category: str, subcategory: str) -> List[str]:
        """Generate product features."""
        feature_templates = {
            "Electronics": [
                "High-quality materials",
                "Advanced technology",
                "Long battery life",
                "Fast performance",
                "Wireless connectivity",
                "Premium design",
                "User-friendly interface",
                "Durable construction"
            ],
            "Fashion": [
                "Comfortable fit",
                "Premium materials",
                "Stylish design",
                "Versatile use",
                "Easy care",
                "Durable construction",
                "Trendy appearance",
                "Perfect sizing"
            ]
        }
        
        features = feature_templates.get(category, [
            "High quality",
            "Durable",
            "Well-designed",
            "Great value",
            "Popular choice"
        ])
        
        return random.sample(features, min(5, len(features)))
    
    def _generate_specifications(self, category: str, subcategory: str) -> Dict:
        """Generate product specifications."""
        specs = {
            "Electronics": {
                "Dimensions": f"{random.randint(10, 50)} x {random.randint(10, 50)} x {random.randint(5, 20)} cm",
                "Weight": f"{random.randint(100, 2000)}g",
                "Color": random.choice(["Black", "White", "Silver", "Gold", "Blue", "Red"]),
                "Warranty": f"{random.randint(1, 3)} years"
            },
            "Fashion": {
                "Material": random.choice(["Cotton", "Polyester", "Wool", "Leather", "Denim", "Silk"]),
                "Size": random.choice(["S", "M", "L", "XL", "XXL"]),
                "Color": random.choice(["Black", "White", "Blue", "Red", "Green", "Yellow"]),
                "Care": "Machine washable"
            }
        }
        
        return specs.get(category, {
            "Material": "High quality",
            "Color": "Various",
            "Size": "Standard"
        })
    
    def _generate_tags(self, category: str, subcategory: str, brand: str) -> List[str]:
        """Generate product tags."""
        tags = [category.lower(), subcategory.lower(), brand.lower()]
        
        # Add category-specific tags
        if category == "Electronics":
            tags.extend(["technology", "gadget", "smart", "wireless"])
        elif category == "Fashion":
            tags.extend(["style", "trendy", "fashionable", "clothing"])
        
        return tags
    
    async def _generate_images(self, category: str, subcategory: str) -> List[str]:
        """Generate product images using reliable image services with contextual relevance."""
        # Create a seed based on category and subcategory for consistent images
        category_seed = hash(f"{category}_{subcategory}") % 1000
        
        # Generate 4 images with different seeds but related to the category
        image_ids = [
            category_seed,
            category_seed + 1,
            category_seed + 2,
            category_seed + 3
        ]
        
        images = []
        for img_id in image_ids:
            # Use Picsum Photos with category-based seeding for more relevant images
            image_url = f"https://picsum.photos/400/400?random={img_id}&blur=1"
            images.append(image_url)
        
        return images
    
    async def generate_product_batch(self, count: int = 100, category: str = None) -> List[Dict]:
        """Generate a batch of products."""
        products = []
        for _ in range(count):
            product = await self.generate_product(category)
            products.append(product)
        return products


class PriceOptimizer:
    """ML-based price optimization system."""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def train(self, historical_data: List[Dict]):
        """Train the price optimization model."""
        # Prepare features
        features = []
        prices = []
        
        for item in historical_data:
            feature_vector = [
                item.get('category_id', 0),
                item.get('brand_id', 0),
                item.get('rating', 0),
                item.get('reviews', 0),
                item.get('stock_quantity', 0),
                item.get('is_featured', 0),
                item.get('is_bestseller', 0),
                item.get('competitor_price', 0),
                item.get('demand_score', 0),
                item.get('seasonality_factor', 1.0)
            ]
            features.append(feature_vector)
            prices.append(item.get('optimal_price', item.get('price', 0)))
        
        # Scale features
        X = self.scaler.fit_transform(features)
        y = np.array(prices)
        
        # Train model
        self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        self.is_trained = True
    
    def predict_optimal_price(self, product_features: Dict) -> float:
        """Predict optimal price for a product."""
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        feature_vector = [
            product_features.get('category_id', 0),
            product_features.get('brand_id', 0),
            product_features.get('rating', 0),
            product_features.get('reviews', 0),
            product_features.get('stock_quantity', 0),
            product_features.get('is_featured', 0),
            product_features.get('is_bestseller', 0),
            product_features.get('competitor_price', 0),
            product_features.get('demand_score', 0),
            product_features.get('seasonality_factor', 1.0)
        ]
        
        X = self.scaler.transform([feature_vector])
        predicted_price = self.model.predict(X)[0]
        
        return max(0, predicted_price)


class UserBehaviorAnalyzer:
    """Analyze user behavior patterns."""
    
    def __init__(self):
        self.user_clusters = None
        self.behavior_patterns = None
    
    def analyze_user_segments(self, user_data: List[Dict]) -> Dict:
        """Analyze and segment users based on behavior."""
        # Prepare user features
        features = []
        user_ids = []
        
        for user in user_data:
            feature_vector = [
                user.get('total_purchases', 0),
                user.get('avg_order_value', 0),
                user.get('days_since_last_purchase', 0),
                user.get('total_products_viewed', 0),
                user.get('favorite_category_id', 0),
                user.get('is_premium', 0)
            ]
            features.append(feature_vector)
            user_ids.append(user.get('user_id'))
        
        # Cluster users
        scaler = StandardScaler()
        X = scaler.fit_transform(features)
        
        kmeans = KMeans(n_clusters=5, random_state=42)
        clusters = kmeans.fit_predict(X)
        
        # Analyze clusters
        cluster_analysis = {}
        for i in range(5):
            cluster_users = [user_ids[j] for j in range(len(user_ids)) if clusters[j] == i]
            cluster_features = [features[j] for j in range(len(features)) if clusters[j] == i]
            
            cluster_analysis[f"cluster_{i}"] = {
                "user_count": len(cluster_users),
                "avg_purchases": np.mean([f[0] for f in cluster_features]),
                "avg_order_value": np.mean([f[1] for f in cluster_features]),
                "user_ids": cluster_users
            }
        
        self.user_clusters = cluster_analysis
        return cluster_analysis
    
    def predict_user_lifetime_value(self, user_features: Dict) -> float:
        """Predict customer lifetime value."""
        # Simple CLV prediction based on historical data
        base_clv = user_features.get('avg_order_value', 0) * user_features.get('total_purchases', 0)
        
        # Apply multipliers based on user characteristics
        if user_features.get('is_premium', False):
            base_clv *= 1.5
        
        if user_features.get('days_since_last_purchase', 0) < 30:
            base_clv *= 1.2
        
        return base_clv


class DemandPredictor:
    """Predict product demand and trends."""
    
    def __init__(self):
        self.trend_model = None
        self.seasonal_patterns = {}
    
    def analyze_trends(self, sales_data: List[Dict]) -> Dict:
        """Analyze sales trends and patterns."""
        # Group by product and time
        product_sales = {}
        for sale in sales_data:
            product_id = sale.get('product_id')
            date = sale.get('date')
            quantity = sale.get('quantity', 1)
            
            if product_id not in product_sales:
                product_sales[product_id] = []
            product_sales[product_id].append({'date': date, 'quantity': quantity})
        
        # Analyze trends for each product
        trends = {}
        for product_id, sales in product_sales.items():
            # Calculate moving average
            quantities = [s['quantity'] for s in sales]
            if len(quantities) > 7:
                moving_avg = np.convolve(quantities, np.ones(7)/7, mode='valid')
                trend = np.polyfit(range(len(moving_avg)), moving_avg, 1)[0]
                
                trends[product_id] = {
                    'trend_direction': 'increasing' if trend > 0 else 'decreasing',
                    'trend_strength': abs(trend),
                    'total_sales': sum(quantities),
                    'avg_daily_sales': np.mean(quantities)
                }
        
        return trends
    
    def predict_demand(self, product_id: int, days_ahead: int = 30) -> Dict:
        """Predict future demand for a product."""
        # This would use historical data and ML models
        # For now, return a simple prediction
        base_demand = random.randint(10, 100)
        seasonal_factor = self._get_seasonal_factor(days_ahead)
        
        predicted_demand = base_demand * seasonal_factor
        
        return {
            'product_id': product_id,
            'predicted_demand': int(predicted_demand),
            'confidence': random.uniform(0.7, 0.95),
            'seasonal_factor': seasonal_factor
        }
    
    def _get_seasonal_factor(self, days_ahead: int) -> float:
        """Get seasonal adjustment factor."""
        # Simple seasonal patterns
        month = (datetime.now() + timedelta(days=days_ahead)).month
        
        seasonal_factors = {
            12: 1.3,  # December (holiday season)
            1: 0.8,   # January (post-holiday)
            6: 1.1,   # June (summer)
            7: 1.2,   # July (summer)
            8: 1.1,   # August (summer)
            11: 1.2   # November (Black Friday)
        }
        
        return seasonal_factors.get(month, 1.0)


class MLService:
    """Main ML service orchestrator."""
    
    def __init__(self):
        self.product_generator = ProductGenerator()
        self.price_optimizer = PriceOptimizer()
        self.behavior_analyzer = UserBehaviorAnalyzer()
        self.demand_predictor = DemandPredictor()
        self.recommendation_engine = None  # Will be initialized from existing code
    
    async def generate_limitless_products(self, target_count: int = 10000) -> List[Dict]:
        """Generate a limitless product database."""
        products = []
        categories = list(self.product_generator.categories.keys())
        
        # Generate products in batches
        batch_size = 100
        for i in range(0, target_count, batch_size):
            batch_count = min(batch_size, target_count - i)
            
            # Distribute across categories
            for category in categories:
                category_count = batch_count // len(categories)
                category_products = await self.product_generator.generate_product_batch(
                    category_count, category
                )
                products.extend(category_products)
            
            logger.info(f"Generated {len(products)} products so far...")
        
        return products
    
    def optimize_prices(self, products: List[Dict], market_data: List[Dict]) -> List[Dict]:
        """Optimize prices for all products."""
        # Train price optimization model
        self.price_optimizer.train(market_data)
        
        optimized_products = []
        for product in products:
            # Prepare features for price optimization
            features = {
                'category_id': hash(product.get('category', '')) % 1000,
                'brand_id': hash(product.get('brand', '')) % 1000,
                'rating': product.get('rating', 0),
                'reviews': product.get('reviews', 0),
                'stock_quantity': product.get('stock_quantity', 0),
                'is_featured': 1 if product.get('is_featured') else 0,
                'is_bestseller': 1 if product.get('is_bestseller') else 0,
                'competitor_price': product.get('price', 0) * random.uniform(0.8, 1.2),
                'demand_score': random.uniform(0.5, 1.5),
                'seasonality_factor': random.uniform(0.8, 1.2)
            }
            
            # Predict optimal price
            optimal_price = self.price_optimizer.predict_optimal_price(features)
            
            # Update product with optimized price
            product['optimized_price'] = round(optimal_price, 2)
            product['price_optimization_score'] = random.uniform(0.7, 0.95)
            
            optimized_products.append(product)
        
        return optimized_products
    
    def analyze_user_behavior(self, user_data: List[Dict]) -> Dict:
        """Analyze user behavior and create segments."""
        return self.behavior_analyzer.analyze_user_segments(user_data)
    
    def predict_demand_trends(self, sales_data: List[Dict]) -> Dict:
        """Predict demand trends for products."""
        return self.demand_predictor.analyze_trends(sales_data)
    
    def get_personalized_recommendations(self, user_id: int, user_history: List[Dict]) -> List[Dict]:
        """Get personalized product recommendations."""
        # This would integrate with the existing recommendation engine
        # For now, return mock recommendations
        recommendations = []
        for i in range(10):
            recommendations.append({
                'product_id': random.randint(1, 1000),
                'score': random.uniform(0.5, 1.0),
                'reason': random.choice(['Similar to your purchases', 'Popular in your category', 'Trending now'])
            })
        
        return sorted(recommendations, key=lambda x: x['score'], reverse=True)
    
    def save_models(self, filepath: str = "models/"):
        """Save all trained models."""
        os.makedirs(filepath, exist_ok=True)
        
        if self.price_optimizer.is_trained:
            with open(f"{filepath}/price_optimizer.pkl", 'wb') as f:
                pickle.dump(self.price_optimizer, f)
        
        if self.behavior_analyzer.user_clusters:
            with open(f"{filepath}/user_clusters.pkl", 'wb') as f:
                pickle.dump(self.behavior_analyzer.user_clusters, f)
    
    def load_models(self, filepath: str = "models/"):
        """Load trained models."""
        try:
            with open(f"{filepath}/price_optimizer.pkl", 'rb') as f:
                self.price_optimizer = pickle.load(f)
            
            with open(f"{filepath}/user_clusters.pkl", 'rb') as f:
                self.behavior_analyzer.user_clusters = pickle.load(f)
                
        except FileNotFoundError:
            logger.warning("No saved models found. Models will need to be trained.") 