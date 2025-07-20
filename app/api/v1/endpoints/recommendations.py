"""
Recommendation endpoints for AI-powered product recommendations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.ai.recommendation_engine import recommendation_engine

router = APIRouter()


@router.get("/user/{user_id}")
async def get_user_recommendations(
    user_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get personalized recommendations for a user."""
    try:
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get hybrid recommendations
        recommendations = recommendation_engine.get_hybrid_recommendations(user_id, limit)
        
        return {
            "user_id": user_id,
            "recommendations": recommendations,
            "total": len(recommendations)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )


@router.get("/product/{product_id}/similar")
async def get_similar_products(
    product_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get similar products based on content-based filtering."""
    try:
        # Get item-based recommendations
        item_based = recommendation_engine.get_item_based_recommendations(product_id, limit)
        
        # Get content-based recommendations
        content_based = recommendation_engine.get_content_based_recommendations(product_id, limit)
        
        return {
            "product_id": product_id,
            "item_based": item_based,
            "content_based": content_based
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error finding similar products: {str(e)}"
        )


@router.get("/trending")
async def get_trending_products(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get trending products based on recent activity."""
    try:
        # This would typically analyze recent user behaviors
        # For now, return a placeholder response
        return {
            "message": "Trending products - to be implemented with real-time analytics",
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting trending products: {str(e)}"
        )


@router.post("/track-behavior")
async def track_user_behavior(
    user_id: int,
    product_id: int,
    behavior_type: str,
    db: Session = Depends(get_db)
):
    """Track user behavior for recommendation training."""
    try:
        from app.models.recommendation import UserBehavior
        
        # Create behavior record
        behavior = UserBehavior(
            user_id=user_id,
            product_id=product_id,
            behavior_type=behavior_type
        )
        
        db.add(behavior)
        db.commit()
        
        return {"message": "Behavior tracked successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error tracking behavior: {str(e)}"
        )