#!/usr/bin/env python3
"""
Script to create a test user for the ecommerce platform.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from datetime import datetime, timezone

def create_test_user():
    """Create a test user in the database."""
    db = SessionLocal()
    
    try:
        # Check if test user already exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("✅ Test user already exists:")
            print(f"   Email: {existing_user.email}")
            print(f"   Username: {existing_user.username}")
            print(f"   Name: {existing_user.first_name} {existing_user.last_name}")
            return
        
        # Create test user
        test_user = User(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            hashed_password=get_password_hash("testpass123"),
            is_active=True,
            role=UserRole.CUSTOMER,
            created_at=datetime.now(timezone.utc)
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print("✅ Test user created successfully!")
        print(f"   Email: {test_user.email}")
        print(f"   Username: {test_user.username}")
        print(f"   Password: testpass123")
        print(f"   Name: {test_user.first_name} {test_user.last_name}")
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user() 