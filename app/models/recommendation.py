"""
Recommendation models for the AI recommendation system.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class UserBehavior(Base):
    """User behavior tracking model for AI recommendations."""
    
    __tablename__ = "user_behaviors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # Behavior type
    behavior_type = Column(String(50), nullable=False)  # view, add_to_cart, purchase, review, like, share
    
    # Behavior details
    session_id = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(Text, nullable=True)
    
    # Additional context
    context = Column(JSON, nullable=True)  # Page context, search terms, filters, etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="behaviors")


class ProductRecommendation(Base):
    """Product recommendation model for storing AI-generated recommendations."""
    
    __tablename__ = "product_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null for anonymous users
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    recommended_product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # Recommendation details
    recommendation_type = Column(String(50), nullable=False)  # collaborative, content_based, trending, etc.
    score = Column(Float, nullable=False)  # Recommendation confidence score (0-1)
    reason = Column(String(255), nullable=True)  # Human-readable reason for recommendation
    
    # Recommendation metadata
    recommendation_metadata = Column(JSON, nullable=True)  # Algorithm parameters, feature weights, etc.
    
    # Usage tracking
    is_clicked = Column(Boolean, default=False)
    is_purchased = Column(Boolean, default=False)
    click_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    product = relationship("Product", foreign_keys=[product_id])
    recommended_product = relationship("Product", foreign_keys=[recommended_product_id]) 