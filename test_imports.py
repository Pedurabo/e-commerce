#!/usr/bin/env python3
"""
Test script to check if all required modules can be imported.
"""

def test_imports():
    """Test all required imports."""
    print("🧪 Testing imports...")
    print("=" * 50)
    
    try:
        print("📦 Testing config...")
        from app.config import settings
        print("✅ Config imported successfully")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        print("🗄️  Testing database...")
        from app.database import engine, Base, get_db
        print("✅ Database imported successfully")
    except Exception as e:
        print(f"❌ Database import failed: {e}")
        return False
    
    try:
        print("🔐 Testing security...")
        from app.core.security import create_access_token, get_password_hash
        print("✅ Security imported successfully")
    except Exception as e:
        print(f"❌ Security import failed: {e}")
        return False
    
    try:
        print("👥 Testing user models...")
        from app.models.user import User, Admin, UserRole
        print("✅ User models imported successfully")
    except Exception as e:
        print(f"❌ User models import failed: {e}")
        return False
    
    try:
        print("📦 Testing product models...")
        from app.models.product import Product, Category
        print("✅ Product models imported successfully")
    except Exception as e:
        print(f"❌ Product models import failed: {e}")
        return False
    
    try:
        print("📋 Testing order models...")
        from app.models.order import Order, OrderItem, Cart, CartItem
        print("✅ Order models imported successfully")
    except Exception as e:
        print(f"❌ Order models import failed: {e}")
        return False
    
    try:
        print("💳 Testing payment models...")
        from app.models.payment import Payment, PaymentMethod
        print("✅ Payment models imported successfully")
    except Exception as e:
        print(f"❌ Payment models import failed: {e}")
        return False
    
    try:
        print("🤖 Testing recommendation models...")
        from app.models.recommendation import UserBehavior, ProductReview
        print("✅ Recommendation models imported successfully")
    except Exception as e:
        print(f"❌ Recommendation models import failed: {e}")
        return False
    
    try:
        print("📝 Testing user schemas...")
        from app.schemas.user import UserCreate, UserResponse
        print("✅ User schemas imported successfully")
    except Exception as e:
        print(f"❌ User schemas import failed: {e}")
        return False
    
    try:
        print("🔑 Testing auth schemas...")
        from app.schemas.auth import LoginRequest, Token
        print("✅ Auth schemas imported successfully")
    except Exception as e:
        print(f"❌ Auth schemas import failed: {e}")
        return False
    
    try:
        print("🌐 Testing API router...")
        from app.api.v1.api import api_router
        print("✅ API router imported successfully")
    except Exception as e:
        print(f"❌ API router import failed: {e}")
        return False
    
    try:
        print("🔌 Testing auth endpoints...")
        from app.api.v1.endpoints import auth
        print("✅ Auth endpoints imported successfully")
    except Exception as e:
        print(f"❌ Auth endpoints import failed: {e}")
        return False
    
    try:
        print("👤 Testing user endpoints...")
        from app.api.v1.endpoints import users
        print("✅ User endpoints imported successfully")
    except Exception as e:
        print(f"❌ User endpoints import failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All imports successful!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("✅ All modules can be imported successfully!")
    else:
        print("❌ Some modules failed to import!") 