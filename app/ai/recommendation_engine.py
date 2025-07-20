"""
AI-powered recommendation engine for product suggestions.
"""

import random
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
import numpy as np
from datetime import datetime, timedelta

from app.models import Product, User, UserBehavior, ProductRecommendation


class RecommendationEngine:
    def __init__(self):
        self.collaborative_filtering_weight = 0.4
        self.content_based_weight = 0.3
        self.popularity_weight = 0.2
        self.recent_weight = 0.1

    async def get_recommendations(
        self,
        user_id: Optional[int] = None,
        limit: int = 10,
        db: Session = None
    ) -> List[Product]:
        """
        Get personalized product recommendations.
        """
        if not db:
            return []
        
        try:
            # Combine multiple recommendation strategies
            recommendations = []
            
            # 1. Collaborative filtering (if user exists)
            if user_id:
                cf_recommendations = await self._collaborative_filtering(user_id, db)
                recommendations.extend(cf_recommendations)
            
            # 2. Content-based filtering
            cb_recommendations = await self._content_based_filtering(user_id, db)
            recommendations.extend(cb_recommendations)
            
            # 3. Popularity-based recommendations
            pop_recommendations = await self._popularity_based_recommendations(db)
            recommendations.extend(pop_recommendations)
            
            # 4. Recent products
            recent_recommendations = await self._recent_products(db)
            recommendations.extend(recent_recommendations)
            
            # Remove duplicates and score products
            scored_products = self._score_and_rank_products(recommendations, user_id)
            
            # Return top recommendations
            return scored_products[:limit]
            
        except Exception as e:
            print(f"Error in recommendation engine: {e}")
            # Fallback to random recommendations
            return await self._fallback_recommendations(limit, db)

    async def _collaborative_filtering(
        self,
        user_id: int,
        db: Session
    ) -> List[Product]:
        """
        Collaborative filtering based on similar users' behavior.
        """
        try:
            # Get user's behavior history
            user_behaviors = db.query(UserBehavior).filter(
                UserBehavior.user_id == user_id
            ).all()
            
            if not user_behaviors:
                return []
            
            # Find similar users based on behavior patterns
            similar_users = await self._find_similar_users(user_id, db)
            
            # Get products liked by similar users
            recommended_products = []
            for similar_user in similar_users:
                user_products = db.query(UserBehavior).filter(
                    UserBehavior.user_id == similar_user.id,
                    UserBehavior.behavior_type.in_(['view', 'purchase', 'wishlist'])
                ).all()
                
                for behavior in user_products:
                    product = db.query(Product).filter(
                        Product.id == behavior.product_id
                    ).first()
                    if product:
                        recommended_products.append(product)
            
            return recommended_products
            
        except Exception as e:
            print(f"Error in collaborative filtering: {e}")
            return []

    async def _content_based_filtering(
        self,
        user_id: Optional[int],
        db: Session
    ) -> List[Product]:
        """
        Content-based filtering based on product categories and features.
        """
        try:
            if not user_id:
                return []
            
            # Get user's preferred categories
            user_categories = db.query(
                Product.category,
                func.count(UserBehavior.id).label('interaction_count')
            ).join(
                UserBehavior, Product.id == UserBehavior.product_id
            ).filter(
                UserBehavior.user_id == user_id,
                UserBehavior.behavior_type.in_(['view', 'purchase'])
            ).group_by(
                Product.category
            ).order_by(
                func.count(UserBehavior.id).desc()
            ).limit(3).all()
            
            if not user_categories:
                return []
            
            # Get products from preferred categories
            preferred_categories = [cat[0] for cat in user_categories]
            recommended_products = db.query(Product).filter(
                Product.category.in_(preferred_categories)
            ).limit(20).all()
            
            return recommended_products
            
        except Exception as e:
            print(f"Error in content-based filtering: {e}")
            return []

    async def _popularity_based_recommendations(
        self,
        db: Session
    ) -> List[Product]:
        """
        Popularity-based recommendations based on overall product popularity.
        """
        try:
            # Get most popular products based on views and purchases
            popular_products = db.query(
                Product,
                func.count(UserBehavior.id).label('interaction_count')
            ).outerjoin(
                UserBehavior, Product.id == UserBehavior.product_id
            ).group_by(
                Product.id
            ).order_by(
                func.count(UserBehavior.id).desc()
            ).limit(20).all()
            
            return [product[0] for product in popular_products]
            
        except Exception as e:
            print(f"Error in popularity-based recommendations: {e}")
            return []

    async def _recent_products(
        self,
        db: Session
    ) -> List[Product]:
        """
        Recent products recommendations.
        """
        try:
            # Get recently added products
            recent_products = db.query(Product).order_by(
                Product.created_at.desc()
            ).limit(10).all()
            
            return recent_products
            
        except Exception as e:
            print(f"Error in recent products: {e}")
            return []

    async def _find_similar_users(
        self,
        user_id: int,
        db: Session
    ) -> List[User]:
        """
        Find users with similar behavior patterns.
        """
        try:
            # Get current user's behavior
            user_behaviors = db.query(UserBehavior).filter(
                UserBehavior.user_id == user_id
            ).all()
            
            if not user_behaviors:
                return []
            
            # Find users who interacted with similar products
            user_product_ids = [b.product_id for b in user_behaviors]
            
            similar_users = db.query(User).join(
                UserBehavior, User.id == UserBehavior.user_id
            ).filter(
                UserBehavior.product_id.in_(user_product_ids),
                User.id != user_id
            ).distinct().limit(10).all()
            
            return similar_users
            
        except Exception as e:
            print(f"Error finding similar users: {e}")
            return []

    def _score_and_rank_products(
        self,
        products: List[Product],
        user_id: Optional[int]
    ) -> List[Product]:
        """
        Score and rank products based on multiple factors.
        """
        try:
            if not products:
                return []
            
            # Create product scores
            product_scores = {}
            
            for product in products:
                score = 0.0
                
                # Base score
                score += 1.0
                
                # Category preference (if user exists)
                if user_id:
                    # This would be enhanced with actual user preferences
                    score += random.uniform(0, 0.5)
                
                # Price attractiveness (lower prices get higher scores)
                if product.price < 50:
                    score += 0.3
                elif product.price < 100:
                    score += 0.2
                elif product.price < 200:
                    score += 0.1
                
                # Stock availability
                if product.stock > 0:
                    score += 0.2
                
                # Recent products get slight boost
                if product.created_at:
                    days_old = (datetime.utcnow() - product.created_at).days
                    if days_old < 30:
                        score += 0.1
                
                product_scores[product.id] = score
            
            # Sort products by score
            sorted_products = sorted(
                products,
                key=lambda p: product_scores.get(p.id, 0),
                reverse=True
            )
            
            # Remove duplicates while preserving order
            seen_ids = set()
            unique_products = []
            for product in sorted_products:
                if product.id not in seen_ids:
                    seen_ids.add(product.id)
                    unique_products.append(product)
            
            return unique_products
            
        except Exception as e:
            print(f"Error scoring products: {e}")
            return products

    async def _fallback_recommendations(
        self,
        limit: int,
        db: Session
    ) -> List[Product]:
        """
        Fallback recommendations when AI fails.
        """
        try:
            # Get random products as fallback
            products = db.query(Product).limit(limit * 2).all()
            random.shuffle(products)
            return products[:limit]
        except Exception as e:
            print(f"Error in fallback recommendations: {e}")
            return []

    async def record_user_behavior(
        self,
        user_id: int,
        product_id: int,
        behavior_type: str,
        db: Session
    ):
        """
        Record user behavior for recommendation learning.
        """
        try:
            behavior = UserBehavior(
                user_id=user_id,
                product_id=product_id,
                behavior_type=behavior_type,
                timestamp=datetime.utcnow()
            )
            db.add(behavior)
            db.commit()
        except Exception as e:
            print(f"Error recording user behavior: {e}")

    async def update_recommendations(
        self,
        user_id: int,
        db: Session
    ):
        """
        Update stored recommendations for a user.
        """
        try:
            # Get fresh recommendations
            recommendations = await self.get_recommendations(user_id, 20, db)
            
            # Clear old recommendations
            db.query(ProductRecommendation).filter(
                ProductRecommendation.user_id == user_id
            ).delete()
            
            # Store new recommendations
            for i, product in enumerate(recommendations):
                recommendation = ProductRecommendation(
                    user_id=user_id,
                    product_id=product.id,
                    score=1.0 - (i * 0.05),  # Decreasing score
                    created_at=datetime.utcnow()
                )
                db.add(recommendation)
            
            db.commit()
            
        except Exception as e:
            print(f"Error updating recommendations: {e}")


# Global recommendation engine instance
recommendation_engine = RecommendationEngine()


async def get_product_recommendations(
    user_id: Optional[int] = None,
    limit: int = 10,
    db: Session = None
) -> List[Product]:
    """
    Get product recommendations using the AI engine.
    """
    return await recommendation_engine.get_recommendations(user_id, limit, db)


async def record_user_behavior(
    user_id: int,
    product_id: int,
    behavior_type: str,
    db: Session
):
    """
    Record user behavior for AI learning.
    """
    await recommendation_engine.record_user_behavior(
        user_id, product_id, behavior_type, db
    )


async def update_user_recommendations(
    user_id: int,
    db: Session
):
    """
    Update recommendations for a specific user.
    """
    await recommendation_engine.update_recommendations(user_id, db) 