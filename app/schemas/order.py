"""
Order schemas for cart and order management.
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CartItemBase(BaseModel):
    """Base cart item schema."""
    product_id: int
    quantity: int = 1


class CartItemCreate(CartItemBase):
    """Cart item creation schema."""
    pass


class CartItemUpdate(BaseModel):
    """Cart item update schema."""
    quantity: int


class CartItemResponse(CartItemBase):
    """Cart item response schema."""
    id: int
    cart_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """Cart response schema."""
    id: int
    user_id: int
    items: List[CartItemResponse] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    """Base order item schema."""
    product_id: int
    product_name: str
    product_sku: str
    quantity: int
    unit_price: float
    total_price: float


class OrderItemResponse(OrderItemBase):
    """Order item response schema."""
    id: int
    order_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    """Base order schema."""
    billing_first_name: str
    billing_last_name: str
    billing_email: str
    billing_phone: Optional[str] = None
    billing_address: str
    billing_city: str
    billing_state: str
    billing_country: str
    billing_postal_code: str
    shipping_first_name: Optional[str] = None
    shipping_last_name: Optional[str] = None
    shipping_address: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_state: Optional[str] = None
    shipping_country: Optional[str] = None
    shipping_postal_code: Optional[str] = None
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    """Order creation schema."""
    pass


class OrderUpdate(BaseModel):
    """Order update schema."""
    status: Optional[str] = None
    payment_status: Optional[str] = None
    tracking_number: Optional[str] = None
    estimated_delivery: Optional[datetime] = None
    notes: Optional[str] = None


class OrderResponse(OrderBase):
    """Order response schema."""
    id: int
    order_number: str
    user_id: int
    status: str
    payment_status: str
    subtotal: float
    tax_amount: float
    shipping_amount: float
    discount_amount: float
    total_amount: float
    currency: str
    tracking_number: Optional[str] = None
    estimated_delivery: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True 