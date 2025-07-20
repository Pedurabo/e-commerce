"""
Payment models for the ecommerce application.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class PaymentMethodType(str, enum.Enum):
    """Payment method type enumeration."""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    CRYPTO = "crypto"
    BANK_TRANSFER = "bank_transfer"
    DIGITAL_WALLET = "digital_wallet"
    BUY_NOW_PAY_LATER = "buy_now_pay_later"


class PaymentStatus(str, enum.Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    PARTIALLY_REFUNDED = "partially_refunded"


class PaymentMethod(Base):
    """Payment method model for storing user payment methods."""
    
    __tablename__ = "payment_methods"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(PaymentMethodType), nullable=False)
    name = Column(String(255), nullable=False)  # e.g., "Visa ending in 1234"
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Encrypted payment details (varies by type)
    payment_details = Column(JSON, nullable=True)  # Encrypted card details, wallet info, etc.
    
    # Provider-specific information
    provider = Column(String(100), nullable=True)  # e.g., "stripe", "paypal"
    provider_payment_method_id = Column(String(255), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    payments = relationship("Payment", back_populates="payment_method")


class Payment(Base):
    """Payment transaction model."""
    
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"), nullable=True)
    
    # Payment information
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    type = Column(Enum(PaymentMethodType), nullable=False)
    
    # Provider information
    provider = Column(String(100), nullable=False)  # e.g., "stripe", "paypal", "crypto"
    provider_transaction_id = Column(String(255), nullable=True)
    provider_payment_intent_id = Column(String(255), nullable=True)
    
    # Transaction details
    description = Column(Text, nullable=True)
    failure_reason = Column(Text, nullable=True)
    payment_metadata = Column(JSON, nullable=True)  # Additional provider-specific data
    
    # Timestamps
    processed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    order = relationship("Order", back_populates="payments")
    payment_method = relationship("PaymentMethod", back_populates="payments") 