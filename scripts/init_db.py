#!/usr/bin/env python3
"""
Database initialization script.
Creates tables and adds sample data for development.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app.models.user import User, Admin, UserRole
from app.models.product import Product, Category
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.recommendation import UserBehavior, ProductReview
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random


def init_db():
    """Initialize database with tables and sample data."""
    print("🚀 Initializing database...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("⚠️  Database already contains data, skipping initialization")
            return
        
        print("📝 Creating sample data...")
        
        # Create sample users
        users = [
            User(
                email="john.doe@example.com",
                username="johndoe",
                hashed_password=get_password_hash("password123"),
                first_name="John",
                last_name="Doe",
                phone="+1234567890",
                is_active=True,
                is_verified=True,
                role=UserRole.CUSTOMER
            ),
            User(
                email="jane.smith@example.com",
                username="janesmith",
                hashed_password=get_password_hash("password123"),
                first_name="Jane",
                last_name="Smith",
                phone="+1234567891",
                is_active=True,
                is_verified=True,
                role=UserRole.CUSTOMER
            ),
            User(
                email="admin@example.com",
                username="admin",
                hashed_password=get_password_hash("admin123"),
                first_name="Admin",
                last_name="User",
                phone="+1234567892",
                is_active=True,
                is_verified=True,
                role=UserRole.ADMIN
            )
        ]
        
        # Create sample admin
        admin = Admin(
            email="superadmin@example.com",
            username="superadmin",
            hashed_password=get_password_hash("admin123"),
            first_name="Super",
            last_name="Admin",
            is_super_admin=True,
            is_active=True
        )
        
        # Add users and admin to database
        for user in users:
            db.add(user)
        db.add(admin)
        db.commit()
        
        # Create sample categories
        categories = [
            Category(name="Electronics", description="Electronic devices and gadgets"),
            Category(name="Clothing", description="Fashion and apparel"),
            Category(name="Books", description="Books and literature"),
            Category(name="Home & Garden", description="Home improvement and gardening"),
            Category(name="Sports", description="Sports equipment and accessories")
        ]
        
        for category in categories:
            db.add(category)
        db.commit()
        
        # Create sample products
        products = [
            Product(
                name="iPhone 15 Pro",
                description="Latest iPhone with advanced features",
                price=999.99,
                stock_quantity=50,
                category_id=1,
                image_url="https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=400",
                is_active=True
            ),
            Product(
                name="MacBook Air M2",
                description="Powerful laptop with M2 chip",
                price=1199.99,
                stock_quantity=30,
                category_id=1,
                image_url="https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400",
                is_active=True
            ),
            Product(
                name="Nike Air Max",
                description="Comfortable running shoes",
                price=129.99,
                stock_quantity=100,
                category_id=2,
                image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
                is_active=True
            ),
            Product(
                name="The Great Gatsby",
                description="Classic American novel",
                price=12.99,
                stock_quantity=200,
                category_id=3,
                image_url="https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400",
                is_active=True
            ),
            Product(
                name="Garden Tool Set",
                description="Complete set of gardening tools",
                price=89.99,
                stock_quantity=75,
                category_id=4,
                image_url="https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400",
                is_active=True
            ),
            Product(
                name="Basketball",
                description="Professional basketball",
                price=29.99,
                stock_quantity=150,
                category_id=5,
                image_url="https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400",
                is_active=True
            )
        ]
        
        for product in products:
            db.add(product)
        db.commit()
        
        print("✅ Sample data created successfully!")
        print("\n📋 Test Accounts:")
        print("👤 Customer: john.doe@example.com / password123")
        print("👤 Customer: jane.smith@example.com / password123")
        print("👨‍💼 Admin: admin@example.com / admin123")
        print("👑 Super Admin: superadmin@example.com / admin123")
        print("\n🛍️  Sample products created with categories and images")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db() 