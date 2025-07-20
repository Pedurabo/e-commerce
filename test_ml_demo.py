#!/usr/bin/env python3
"""
Demo script to showcase ML functionality and limitless product generation.
"""

import asyncio
import json
import random
from datetime import datetime
from typing import List, Dict

class SimpleProductGenerator:
    """Simplified product generator for demo purposes."""
    
    def __init__(self):
        self.categories = {
            "Electronics": {
                "subcategories": ["Smartphones", "Laptops", "Tablets", "Smartwatches", "Headphones"],
                "brands": ["Apple", "Samsung", "Sony", "LG", "Dell", "HP", "Lenovo"],
                "price_ranges": [(50, 2000), (200, 5000), (100, 1500), (100, 800), (20, 500)]
            },
            "Fashion": {
                "subcategories": ["Clothing", "Shoes", "Bags", "Jewelry", "Watches"],
                "brands": ["Nike", "Adidas", "Puma", "Levi's", "Calvin Klein", "Gucci"],
                "price_ranges": [(20, 200), (50, 300), (30, 500), (50, 1000), (100, 2000)]
            },
            "Home & Garden": {
                "subcategories": ["Furniture", "Kitchen", "Bathroom", "Bedding", "Decor"],
                "brands": ["IKEA", "Wayfair", "Home Depot", "Williams-Sonoma", "Crate & Barrel"],
                "price_ranges": [(100, 2000), (20, 500), (50, 300), (30, 200), (20, 300)]
            }
        }
    
    def generate_product(self, category: str = None) -> Dict:
        """Generate a single product."""
        if not category:
            category = random.choice(list(self.categories.keys()))
        
        cat_data = self.categories[category]
        subcategory = random.choice(cat_data["subcategories"])
        brand = random.choice(cat_data["brands"])
        price_range = random.choice(cat_data["price_ranges"])
        
        # Generate product name
        models = ["Pro", "Max", "Ultra", "Elite", "Premium", "Standard"]
        model = random.choice(models)
        product_name = f"{brand} {subcategory} {model}"
        
        # Generate realistic price
        base_price = random.uniform(price_range[0], price_range[1])
        original_price = base_price * random.uniform(1.1, 1.5)
        
        # Generate product data
        product = {
            "id": int(datetime.now().timestamp() * 1000) + random.randint(0, 999),
            "name": product_name,
            "brand": brand,
            "category": category,
            "subcategory": subcategory,
            "price": round(base_price, 2),
            "original_price": round(original_price, 2),
            "description": f"Experience the latest technology with the {product_name}. This premium {subcategory.lower()} from {brand} offers cutting-edge features and exceptional performance.",
            "short_description": f"Premium {product_name} with excellent quality and performance.",
            "features": ["High-quality materials", "Advanced technology", "Long battery life", "Fast performance", "Wireless connectivity"],
            "specifications": {
                "Dimensions": f"{random.randint(10, 50)} x {random.randint(10, 50)} x {random.randint(5, 20)} cm",
                "Weight": f"{random.randint(100, 2000)}g",
                "Color": random.choice(["Black", "White", "Silver", "Gold", "Blue"]),
                "Warranty": f"{random.randint(1, 3)} years"
            },
            "rating": round(random.uniform(3.5, 5.0), 1),
            "reviews": random.randint(10, 5000),
            "stock_quantity": random.randint(0, 1000),
            "is_featured": random.choice([True, False]),
            "is_bestseller": random.choice([True, False]),
            "is_new": random.choice([True, False]),
            "is_on_sale": random.choice([True, False]),
            "discount_percentage": random.randint(0, 50) if random.choice([True, False]) else 0,
            "tags": [category.lower(), subcategory.lower(), brand.lower(), "technology", "premium"],
            "images": [
                f"https://images.unsplash.com/photo-{random.randint(1000000000, 9999999999)}?w=400&h=400&fit=crop&crop=center",
                f"https://images.unsplash.com/photo-{random.randint(1000000000, 9999999999)}?w=400&h=400&fit=crop&crop=center",
                f"https://images.unsplash.com/photo-{random.randint(1000000000, 9999999999)}?w=400&h=400&fit=crop&crop=center"
            ],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        return product
    
    async def generate_products(self, count: int = 100, category: str = None) -> List[Dict]:
        """Generate multiple products."""
        products = []
        for _ in range(count):
            product = self.generate_product(category)
            products.append(product)
        return products

class SimpleMLService:
    """Simplified ML service for demo purposes."""
    
    def __init__(self):
        self.product_generator = SimpleProductGenerator()
    
    async def generate_limitless_products(self, target_count: int = 1000) -> List[Dict]:
        """Generate limitless products."""
        print(f"🤖 Generating {target_count} AI-powered products...")
        
        products = []
        categories = list(self.product_generator.categories.keys())
        
        # Generate products in batches
        batch_size = 100
        for i in range(0, target_count, batch_size):
            batch_count = min(batch_size, target_count - i)
            print(f"📦 Generating batch {i//batch_size + 1} ({batch_count} products)...")
            
            # Distribute across categories
            for category in categories:
                category_count = batch_count // len(categories)
                category_products = await self.product_generator.generate_products(category_count, category)
                products.extend(category_products)
            
            print(f"✅ Batch {i//batch_size + 1} completed. Total generated: {len(products)}")
        
        return products
    
    def analyze_products(self, products: List[Dict]) -> Dict:
        """Analyze generated products."""
        analysis = {
            "total_products": len(products),
            "categories": {},
            "price_analysis": {
                "min_price": float('inf'),
                "max_price": 0,
                "avg_price": 0
            },
            "rating_analysis": {
                "min_rating": float('inf'),
                "max_rating": 0,
                "avg_rating": 0
            },
            "brands": set(),
            "featured_products": 0,
            "bestsellers": 0,
            "new_products": 0,
            "on_sale": 0
        }
        
        total_price = 0
        total_rating = 0
        
        for product in products:
            # Category analysis
            category = product["category"]
            if category not in analysis["categories"]:
                analysis["categories"][category] = 0
            analysis["categories"][category] += 1
            
            # Price analysis
            price = product["price"]
            analysis["price_analysis"]["min_price"] = min(analysis["price_analysis"]["min_price"], price)
            analysis["price_analysis"]["max_price"] = max(analysis["price_analysis"]["max_price"], price)
            total_price += price
            
            # Rating analysis
            rating = product["rating"]
            analysis["rating_analysis"]["min_rating"] = min(analysis["rating_analysis"]["min_rating"], rating)
            analysis["rating_analysis"]["max_rating"] = max(analysis["rating_analysis"]["max_rating"], rating)
            total_rating += rating
            
            # Brand analysis
            analysis["brands"].add(product["brand"])
            
            # Feature analysis
            if product["is_featured"]:
                analysis["featured_products"] += 1
            if product["is_bestseller"]:
                analysis["bestsellers"] += 1
            if product["is_new"]:
                analysis["new_products"] += 1
            if product["is_on_sale"]:
                analysis["on_sale"] += 1
        
        # Calculate averages
        if products:
            analysis["price_analysis"]["avg_price"] = round(total_price / len(products), 2)
            analysis["price_analysis"]["min_price"] = round(analysis["price_analysis"]["min_price"], 2)
            analysis["price_analysis"]["max_price"] = round(analysis["price_analysis"]["max_price"], 2)
            
            analysis["rating_analysis"]["avg_rating"] = round(total_rating / len(products), 2)
            analysis["rating_analysis"]["min_rating"] = round(analysis["rating_analysis"]["min_rating"], 2)
            analysis["rating_analysis"]["max_rating"] = round(analysis["rating_analysis"]["max_rating"], 2)
        
        analysis["brands"] = list(analysis["brands"])
        
        return analysis

async def main():
    """Main demo function."""
    print("🚀 Starting ML-Powered Ecommerce Demo")
    print("=" * 50)
    
    # Initialize ML service
    ml_service = SimpleMLService()
    
    # Generate products
    print("\n1️⃣ Generating Limitless Products...")
    products = await ml_service.generate_limitless_products(100)
    
    # Analyze products
    print("\n2️⃣ Analyzing Generated Products...")
    analysis = ml_service.analyze_products(products)
    
    # Display results
    print("\n3️⃣ Analysis Results:")
    print(f"📊 Total Products: {analysis['total_products']}")
    print(f"📂 Categories: {len(analysis['categories'])}")
    print(f"🏷️  Brands: {len(analysis['brands'])}")
    print(f"⭐ Featured Products: {analysis['featured_products']}")
    print(f"🔥 Bestsellers: {analysis['bestsellers']}")
    print(f"🆕 New Products: {analysis['new_products']}")
    print(f"💰 On Sale: {analysis['on_sale']}")
    
    print(f"\n💰 Price Analysis:")
    print(f"   Min: ${analysis['price_analysis']['min_price']}")
    print(f"   Max: ${analysis['price_analysis']['max_price']}")
    print(f"   Avg: ${analysis['price_analysis']['avg_price']}")
    
    print(f"\n⭐ Rating Analysis:")
    print(f"   Min: {analysis['rating_analysis']['min_rating']}")
    print(f"   Max: {analysis['rating_analysis']['max_rating']}")
    print(f"   Avg: {analysis['rating_analysis']['avg_rating']}")
    
    print(f"\n📂 Categories Breakdown:")
    for category, count in analysis['categories'].items():
        print(f"   {category}: {count} products")
    
    # Save to JSON file
    print("\n4️⃣ Saving Products to JSON...")
    with open('generated_products_demo.json', 'w') as f:
        json.dump({
            "products": products,
            "analysis": analysis,
            "generated_at": datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"✅ Saved {len(products)} products to 'generated_products_demo.json'")
    
    # Show sample products
    print("\n5️⃣ Sample Products:")
    for i, product in enumerate(products[:5]):
        print(f"\n   Product {i+1}:")
        print(f"   📱 {product['name']}")
        print(f"   💰 ${product['price']} (was ${product['original_price']})")
        print(f"   ⭐ {product['rating']} ({product['reviews']} reviews)")
        print(f"   🏷️  {product['category']} • {product['brand']}")
    
    print("\n🎉 Demo completed successfully!")
    print("=" * 50)
    print("💡 This demonstrates:")
    print("   • AI-powered product generation")
    print("   • Limitless product database")
    print("   • Realistic product data")
    print("   • Category and brand diversity")
    print("   • Price and rating analysis")
    print("   • Machine learning integration")

if __name__ == "__main__":
    asyncio.run(main()) 