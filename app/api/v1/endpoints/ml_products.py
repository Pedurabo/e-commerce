"""
ML-powered product generation and management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
import asyncio
import json

from app.database import get_db
from app.ai.ml_service import MLService
from app.schemas.product import ProductCreate, ProductResponse, MLProductResponse
from app.models.product import Product
from app.core.security import get_current_user

router = APIRouter()
ml_service = MLService()

@router.post("/generate-products")
async def generate_products(
    count: int = 100,
    category: Optional[str] = None,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Generate AI-powered products."""
    try:
        # Generate products using ML service
        products = await ml_service.generate_limitless_products(count)
        
        # Store in database
        stored_products = []
        for product_data in products:
            # Convert to ProductCreate schema with proper field mapping
            product_create = ProductCreate(
                name=product_data["name"],
                description=product_data["description"],
                short_description=product_data["short_description"],
                sku=f"SKU-{product_data['name'].replace(' ', '-').upper()}-{product_data['brand'].replace(' ', '-').upper()}",
                price=product_data["price"],
                sale_price=product_data["original_price"] if product_data["is_on_sale"] else None,
                cost_price=product_data["price"] * 0.6,  # Assume 40% margin
                stock_quantity=product_data["stock_quantity"],
                weight=1.0,  # Default weight
                dimensions="10x10x5 cm",  # Default dimensions
                category_id=hash(product_data["category"]) % 1000 + 1,  # Generate category_id from category name
                is_featured=product_data["is_featured"],
                is_bestseller=product_data["is_bestseller"],
                tags=", ".join(product_data["tags"]) if product_data["tags"] else "",
                meta_title=product_data["name"],
                meta_description=product_data["short_description"]
            )
            
            # Create product in database
            db_product = Product(**product_create.model_dump())
            db.add(db_product)
            stored_products.append(db_product)
        
        db.commit()
        
        return {
            "message": f"Successfully generated {len(stored_products)} products",
            "products_count": len(stored_products),
            "category": category
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to generate products: {str(e)}")

@router.get("/products/limitless")
async def get_limitless_products(
    page: int = 1,
    limit: int = 50,
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    sort_order: Optional[str] = "desc",
    db: Session = Depends(get_db)
):
    """Get limitless products with advanced filtering."""
    try:
        # Build query
        query = db.query(Product)
        
        # Apply filters
        if category:
            query = query.filter(Product.category == category)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (Product.name.ilike(search_filter)) |
                (Product.description.ilike(search_filter)) |
                (Product.brand.ilike(search_filter)) |
                (Product.tags.any(lambda x: search.lower() in x.lower()))
            )
        
        # Apply sorting
        if sort_by == "price":
            if sort_order == "asc":
                query = query.order_by(Product.price.asc())
            else:
                query = query.order_by(Product.price.desc())
        elif sort_by == "rating":
            if sort_order == "asc":
                query = query.order_by(Product.rating.asc())
            else:
                query = query.order_by(Product.rating.desc())
        elif sort_by == "reviews":
            if sort_order == "asc":
                query = query.order_by(Product.reviews.asc())
            else:
                query = query.order_by(Product.reviews.desc())
        else:  # created_at
            if sort_order == "asc":
                query = query.order_by(Product.created_at.asc())
            else:
                query = query.order_by(Product.created_at.desc())
        
        # Apply pagination
        total = query.count()
        products = query.offset((page - 1) * limit).limit(limit).all()
        
        # Convert to ML response format
        product_responses = []
        for product in products:
            # Convert database product to ML format
            ml_product = MLProductResponse(
                id=product.id,
                name=product.name,
                description=product.description or "",
                short_description=product.short_description or "",
                price=float(product.price),
                original_price=float(product.sale_price) if product.sale_price else float(product.price),
                category=f"Category {product.category_id}",  # Convert category_id to string
                subcategory="General",
                brand="Generic Brand",
                rating=4.5,  # Default rating
                reviews=100,  # Default reviews
                stock_quantity=product.stock_quantity,
                is_featured=product.is_featured,
                is_bestseller=product.is_bestseller,
                is_new=True,  # Default to new
                is_on_sale=product.sale_price is not None,
                discount_percentage=20.0 if product.sale_price else 0.0,
                tags=product.tags.split(", ") if product.tags else [],
                images=[f"https://picsum.photos/400/400?random={hash(product.name + str(product.category_id)) % 1000}&blur=1"],
                features=["High Quality", "Durable", "Modern Design"],
                specifications={"Size": "Standard", "Material": "Premium", "Warranty": "1 Year"},
                created_at=product.created_at.isoformat() if product.created_at else "",
                updated_at=product.updated_at.isoformat() if product.updated_at else ""
            )
            product_responses.append(ml_product)
        
        return {
            "products": product_responses,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch products: {str(e)}")

@router.post("/products/optimize-prices")
async def optimize_product_prices(
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Optimize product prices using ML."""
    try:
        # Get all products
        products = db.query(Product).all()
        
        # Convert to dict format for ML service
        products_data = []
        for product in products:
            products_data.append({
                "id": product.id,
                "category_id": hash(product.category) % 1000,
                "brand_id": hash(product.brand) % 1000,
                "rating": product.rating,
                "reviews": product.reviews,
                "stock_quantity": product.stock_quantity,
                "is_featured": 1 if product.is_featured else 0,
                "is_bestseller": 1 if product.is_bestseller else 0,
                "price": product.price,
                "original_price": product.original_price
            })
        
        # Generate mock market data for training
        market_data = []
        for product in products_data:
            market_data.append({
                "category_id": product["category_id"],
                "brand_id": product["brand_id"],
                "rating": product["rating"],
                "reviews": product["reviews"],
                "stock_quantity": product["stock_quantity"],
                "is_featured": product["is_featured"],
                "is_bestseller": product["is_bestseller"],
                "competitor_price": product["price"] * 0.9,  # Mock competitor price
                "demand_score": 1.0,  # Mock demand score
                "seasonality_factor": 1.0,  # Mock seasonality
                "optimal_price": product["price"] * 1.1  # Mock optimal price
            })
        
        # Optimize prices
        optimized_products = ml_service.optimize_prices(products_data, market_data)
        
        # Update database with optimized prices
        updated_count = 0
        for optimized_product in optimized_products:
            product = db.query(Product).filter(Product.id == optimized_product["id"]).first()
            if product:
                product.price = optimized_product["optimized_price"]
                updated_count += 1
        
        db.commit()
        
        return {
            "message": f"Successfully optimized prices for {updated_count} products",
            "updated_count": updated_count
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to optimize prices: {str(e)}")

@router.get("/products/recommendations/{user_id}")
async def get_personalized_recommendations(
    user_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get personalized product recommendations."""
    try:
        # Mock user history (in real app, this would come from database)
        user_history = [
            {"product_id": 1, "action": "purchase", "timestamp": "2024-01-01"},
            {"product_id": 5, "action": "view", "timestamp": "2024-01-02"},
            {"product_id": 10, "action": "add_to_cart", "timestamp": "2024-01-03"}
        ]
        
        # Get recommendations
        recommendations = ml_service.get_personalized_recommendations(user_id, user_history)
        
        # Get product details for recommendations
        recommended_products = []
        for rec in recommendations[:limit]:
            product = db.query(Product).filter(Product.id == rec["product_id"]).first()
            if product:
                recommended_products.append({
                    "product": ProductResponse(
                        id=product.id,
                        name=product.name,
                        description=product.description,
                        short_description=product.short_description,
                        price=product.price,
                        original_price=product.original_price,
                        category=product.category,
                        subcategory=product.subcategory,
                        brand=product.brand,
                        rating=product.rating,
                        reviews=product.reviews,
                        stock_quantity=product.stock_quantity,
                        is_featured=product.is_featured,
                        is_bestseller=product.is_bestseller,
                        is_new=product.is_new,
                        is_on_sale=product.is_on_sale,
                        discount_percentage=product.discount_percentage,
                        tags=product.tags,
                        images=product.images,
                        features=product.features,
                        specifications=product.specifications,
                        created_at=product.created_at,
                        updated_at=product.updated_at
                    ),
                    "score": rec["score"],
                    "reason": rec["reason"]
                })
        
        return {
            "user_id": user_id,
            "recommendations": recommended_products
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")

@router.get("/analytics/user-segments")
async def analyze_user_segments(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Analyze user behavior and create segments."""
    try:
        # Mock user data (in real app, this would come from database)
        user_data = [
            {"user_id": 1, "total_purchases": 10, "avg_order_value": 150, "days_since_last_purchase": 5, "total_products_viewed": 50, "favorite_category_id": 1, "is_premium": True},
            {"user_id": 2, "total_purchases": 5, "avg_order_value": 80, "days_since_last_purchase": 30, "total_products_viewed": 20, "favorite_category_id": 2, "is_premium": False},
            {"user_id": 3, "total_purchases": 20, "avg_order_value": 300, "days_since_last_purchase": 2, "total_products_viewed": 100, "favorite_category_id": 1, "is_premium": True}
        ]
        
        # Analyze user segments
        segments = ml_service.analyze_user_behavior(user_data)
        
        return {
            "user_segments": segments,
            "total_users": len(user_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze user segments: {str(e)}")

@router.get("/analytics/demand-trends")
async def get_demand_trends(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get demand trends and predictions."""
    try:
        # Mock sales data (in real app, this would come from database)
        sales_data = [
            {"product_id": 1, "date": "2024-01-01", "quantity": 10},
            {"product_id": 1, "date": "2024-01-02", "quantity": 15},
            {"product_id": 2, "date": "2024-01-01", "quantity": 5},
            {"product_id": 2, "date": "2024-01-02", "quantity": 8}
        ]
        
        # Analyze trends
        trends = ml_service.predict_demand_trends(sales_data)
        
        return {
            "demand_trends": trends,
            "analysis_date": "2024-01-01"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get demand trends: {str(e)}")

@router.post("/models/save")
async def save_ml_models(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Save trained ML models."""
    try:
        ml_service.save_models()
        return {"message": "ML models saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save models: {str(e)}")

@router.post("/models/load")
async def load_ml_models(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Load trained ML models."""
    try:
        ml_service.load_models()
        return {"message": "ML models loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load models: {str(e)}") 