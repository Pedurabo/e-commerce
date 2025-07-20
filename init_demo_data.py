#!/usr/bin/env python3
"""
Initialize database with demo data for testing.
"""

import asyncio
import random
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app.models import User, Product, Category
from app.core.security import get_password_hash

def create_demo_data():
    """Create demo users and products."""
    db = SessionLocal()
    
    try:
        # Create demo categories
        categories = [
            "Electronics",
            "Clothing", 
            "Home & Garden",
            "Sports",
            "Books",
            "Toys",
            "Beauty",
            "Automotive"
        ]
        
        category_objects = []
        for cat_name in categories:
            category = Category(
                name=cat_name,
                description=f"Products in {cat_name} category",
                slug=cat_name.lower().replace(" ", "-"),
                is_active=True
            )
            db.add(category)
            category_objects.append(category)
        
        db.commit()
        
        # Create demo users
        demo_users = [
            {
                "name": "John Customer",
                "email": "customer@example.com",
                "password": "password123",
                "user_type": "customer"
            },
            {
                "name": "Admin User",
                "email": "admin@example.com", 
                "password": "admin123",
                "user_type": "admin"
            }
        ]
        
        for user_data in demo_users:
            hashed_password = get_password_hash(user_data["password"])
            # Split name into first and last name
            name_parts = user_data["name"].split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""
            username = user_data["email"].split("@")[0]
            
            user = User(
                email=user_data["email"],
                username=username,
                hashed_password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                role=user_data["user_type"],
                is_active=True,
                is_verified=True
            )
            db.add(user)
        
        db.commit()
        
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
        
        for i, name in enumerate(product_names):
            category_obj = random.choice(category_objects)
            price = round(random.uniform(9.99, 999.99), 2)
            stock = random.randint(0, 100)
            
            product = Product(
                name=name,
                description=f"High-quality {name.lower()} with premium features and excellent durability.",
                sku=f"SKU-{i+1:04d}",
                price=price,
                stock_quantity=stock,
                stock=stock,  # Alias field
                category_id=category_obj.id,
                image_url=f"https://picsum.photos/400/400?random={i}",
                status="active",
                is_featured=random.choice([True, False]),
                is_bestseller=random.choice([True, False]),
                created_at=datetime.utcnow()
            )
            db.add(product)
        
        db.commit()
        
        print("✅ Demo data created successfully!")
        print(f"📦 Created {len(product_names)} products")
        print(f"👥 Created {len(demo_users)} users")
        print(f"📂 Created {len(categories)} categories")
        
        # Print login credentials
        print("\n🔑 Login Credentials:")
        print("Customer: customer@example.com / password123")
        print("Admin: admin@example.com / admin123")
        
    except Exception as e:
        print(f"❌ Error creating demo data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_data() 