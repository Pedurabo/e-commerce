#!/usr/bin/env python3
"""
Simple script to add products to the database.
"""

import random
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Product

def add_products():
    """Add demo products to the database."""
    db = SessionLocal()
    
    try:
        # Create demo products
        product_names = [
            "Wireless Bluetooth Headphones",
            "Smart Fitness Watch", 
            "Organic Cotton T-Shirt",
            "Stainless Steel Water Bottle",
            "Wireless Charging Pad",
            "Yoga Mat",
            "Laptop Stand",
            "Mechanical Keyboard",
            "Gaming Mouse",
            "USB-C Cable",
            "Power Bank",
            "Bluetooth Speaker",
            "Smart Home Hub",
            "Security Camera",
            "Robot Vacuum",
            "Air Purifier",
            "Coffee Maker",
            "Blender",
            "Toaster",
            "Microwave"
        ]
        
        categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Beauty", "Automotive"]
        
        for i, name in enumerate(product_names):
            price = round(random.uniform(9.99, 999.99), 2)
            stock = random.randint(0, 100)
            category = random.choice(categories)
            
            product = Product(
                name=name,
                description=f"High-quality {name.lower()} with premium features and excellent durability.",
                sku=f"SKU-{i+1:04d}",
                price=price,
                stock_quantity=stock,
                category_id=1,  # Default category ID
                image_url=f"https://picsum.photos/400/400?random={i}",
                status="active",
                is_featured=random.choice([True, False]),
                is_bestseller=random.choice([True, False]),
                created_at=datetime.now(timezone.utc)
            )
            db.add(product)
        
        db.commit()
        
        print("✅ Products added successfully!")
        print(f"📦 Added {len(product_names)} products")
        
    except Exception as e:
        print(f"❌ Error adding products: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_products() 