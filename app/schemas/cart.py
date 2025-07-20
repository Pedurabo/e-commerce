"""
Cart schemas for shopping cart management.
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CartItemCreate(BaseModel):
    """Cart item creation schema."""
    product_id: int
    quantity: int = 1


class CartItemResponse(BaseModel):
    """Cart item response schema."""
    id: int
    product_id: int
    quantity: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CartItemDetail(BaseModel):
    """Cart item with product details."""
    id: int
    product_id: int
    product_name: str
    product_price: float
    quantity: int
    total: float


class CartResponse(BaseModel):
    """Cart response schema."""
    cart_id: int
    user_id: int
    items: List[CartItemDetail]
    total: float
    item_count: int 