"""
Payment schemas for payment method and transaction management.
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class PaymentMethodBase(BaseModel):
    """Base payment method schema."""
    type: str
    name: str
    is_default: bool = False


class PaymentMethodCreate(PaymentMethodBase):
    """Payment method creation schema."""
    payment_details: Optional[Dict[str, Any]] = None
    provider: Optional[str] = None


class PaymentMethodUpdate(BaseModel):
    """Payment method update schema."""
    name: Optional[str] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None


class PaymentMethodResponse(PaymentMethodBase):
    """Payment method response schema."""
    id: int
    user_id: int
    is_active: bool
    provider: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PaymentBase(BaseModel):
    """Base payment schema."""
    amount: float
    currency: str = "USD"
    type: str
    provider: str
    description: Optional[str] = None


class PaymentCreate(PaymentBase):
    """Payment creation schema."""
    order_id: int
    payment_method_id: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


class PaymentResponse(PaymentBase):
    """Payment response schema."""
    id: int
    order_id: int
    payment_method_id: Optional[int] = None
    status: str
    provider_transaction_id: Optional[str] = None
    provider_payment_intent_id: Optional[str] = None
    failure_reason: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 