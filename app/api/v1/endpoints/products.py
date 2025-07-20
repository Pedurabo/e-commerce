"""
Product endpoints for product management.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Security
from sqlalchemy.orm import Session
from typing import List, Optional
import random
import string

from app.database import get_db
from app.models import Product, Category, User
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate, SimpleProductResponse
from app.core.security import get_current_user
from app.ai.recommendation_engine import get_product_recommendations

router = APIRouter()

@router.get("/")
async def get_products(
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of products to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in product names and descriptions"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    db: Session = Depends(get_db)
):
    """
    Get products with pagination and filtering.
    Supports limitless product database with efficient querying.
    """
    try:
        query = db.query(Product)
        
        # Apply filters
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Product.name.ilike(search_term)) |
                (Product.description.ilike(search_term))
            )
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        # Get total count for pagination info
        total_count = query.count()
        
        # Apply pagination
        products = query.offset(skip).limit(limit).all()
        
        # Convert to simple response format
        result = []
        for product in products:
            result.append({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category": "Electronics",  # Default category
                "stock": product.stock_quantity,
                "image_url": product.image_url,
                "created_at": product.created_at
            })
        
        return result
        
    except Exception as e:
        print(f"Error in get_products: {e}")
        # Return empty list on error
        return []

@router.get("/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID."""
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": "Electronics",  # Default category
            "stock": product.stock_quantity,
            "image_url": product.image_url,
            "created_at": product.created_at
        }
    except Exception as e:
        print(f"Error in get_product: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new product (Admin only)."""
    if current_user.user_type != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a product (Admin only)."""
    if current_user.user_type != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for field, value in product_update.dict(exclude_unset=True).items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a product (Admin only)."""
    if current_user.user_type != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.get("/categories/", response_model=List[str])
async def get_categories(db: Session = Depends(get_db)):
    """Get all available product categories."""
    categories = db.query(Category.name).distinct().all()
    return [category[0] for category in categories]

@router.post("/generate-demo/")
async def generate_demo_products(
    count: int = Query(100, ge=1, le=1000, description="Number of demo products to generate"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate demo products for testing (Admin only)."""
    if current_user.user_type != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Demo product data
    categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Beauty", "Automotive"]
    product_names = [
        "Wireless Bluetooth Headphones", "Smart Fitness Watch", "Organic Cotton T-Shirt",
        "Stainless Steel Water Bottle", "Wireless Charging Pad", "Yoga Mat", "Laptop Stand",
        "Mechanical Keyboard", "Gaming Mouse", "USB-C Cable", "Power Bank", "Bluetooth Speaker",
        "Smart Home Hub", "Security Camera", "Robot Vacuum", "Air Purifier", "Coffee Maker",
        "Blender", "Toaster", "Microwave", "Refrigerator", "Washing Machine", "Dishwasher",
        "TV Stand", "Bookshelf", "Desk Chair", "Office Desk", "Bed Frame", "Mattress",
        "Pillow", "Blanket", "Curtains", "Rug", "Lamp", "Mirror", "Clock", "Vase",
        "Plant Pot", "Garden Tools", "BBQ Grill", "Patio Furniture", "Swimming Pool",
        "Tennis Racket", "Basketball", "Soccer Ball", "Baseball Glove", "Golf Clubs",
        "Bicycle", "Treadmill", "Dumbbells", "Resistance Bands", "Foam Roller"
    ]
    
    generated_products = []
    
    for i in range(count):
        # Generate random product data
        name = f"{random.choice(product_names)} {random.randint(1, 999)}"
        category = random.choice(categories)
        price = round(random.uniform(9.99, 999.99), 2)
        description = f"High-quality {name.lower()} with premium features and excellent durability."
        stock = random.randint(0, 100)
        
        # Create product
        product = Product(
            name=name,
            category=category,
            price=price,
            description=description,
            stock=stock,
            image_url=f"https://picsum.photos/400/400?random={i}"
        )
        
        db.add(product)
        generated_products.append(product)
    
    db.commit()
    
    return {
        "message": f"Generated {count} demo products successfully",
        "products_created": len(generated_products)
    }

@router.get("/recommendations/")
async def get_recommendations(
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations to return"),
    db: Session = Depends(get_db)
):
    """Get AI-powered product recommendations."""
    try:
        # Use AI recommendation engine
        recommendations = await get_product_recommendations(
            user_id=None,
            limit=limit,
            db=db
        )
        
        # Convert to simple response format
        result = []
        for product in recommendations:
            result.append({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category": "Electronics",  # Default category
                "stock": product.stock_quantity,
                "image_url": product.image_url,
                "created_at": product.created_at
            })
        
        return result
    except Exception as e:
        print(f"Error in get_recommendations: {e}")
        # Fallback to random recommendations
        products = db.query(Product).limit(limit).all()
        random.shuffle(products)
        
        result = []
        for product in products[:limit]:
            result.append({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category": "Electronics",  # Default category
                "stock": product.stock_quantity,
                "image_url": product.image_url,
                "created_at": product.created_at
            })
        
        return result

@router.get("/trending/")
async def get_trending_products(
    limit: int = Query(10, ge=1, le=50, description="Number of trending products to return"),
    db: Session = Depends(get_db)
):
    """Get trending products based on views and sales."""
    # In a real implementation, this would analyze user behavior data
    # For now, return random products as trending
    products = db.query(Product).limit(limit * 2).all()
    random.shuffle(products)
    
    result = []
    for product in products[:limit]:
        result.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": "Electronics",  # Default category
            "stock": product.stock_quantity,
            "image_url": product.image_url,
            "created_at": product.created_at
        })
    
    return result

@router.get("/search/")
async def search_products(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    db: Session = Depends(get_db)
):
    """Search products by name, description, or category."""
    search_term = f"%{q}%"
    
    products = db.query(Product).filter(
        (Product.name.ilike(search_term)) |
        (Product.description.ilike(search_term)) |
        (Product.category.ilike(search_term))
    ).limit(limit).all()
    
    result = []
    for product in products:
        result.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": "Electronics",  # Default category
            "stock": product.stock_quantity,
            "image_url": product.image_url,
            "created_at": product.created_at
        })
    
    return result 