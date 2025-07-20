"""
Payment processor utility for handling different payment methods.
"""

import stripe
from typing import Dict, Any, Optional
from app.config import settings


class PaymentProcessor:
    """Payment processor for handling multiple payment methods."""
    
    def __init__(self):
        # Initialize Stripe
        if settings.STRIPE_SECRET_KEY:
            stripe.api_key = settings.STRIPE_SECRET_KEY
    
    async def process_stripe_payment(
        self,
        amount: float,
        currency: str = "usd",
        payment_method_id: str = None,
        customer_id: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Process payment through Stripe."""
        try:
            payment_intent_data = {
                "amount": int(amount * 100),  # Convert to cents
                "currency": currency,
                "metadata": metadata or {}
            }
            
            if payment_method_id:
                payment_intent_data["payment_method"] = payment_method_id
            
            if customer_id:
                payment_intent_data["customer"] = customer_id
            
            payment_intent = stripe.PaymentIntent.create(**payment_intent_data)
            
            return {
                "success": True,
                "payment_intent_id": payment_intent.id,
                "client_secret": payment_intent.client_secret,
                "status": payment_intent.status
            }
        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def process_paypal_payment(
        self,
        amount: float,
        currency: str = "USD",
        return_url: str = None,
        cancel_url: str = None
    ) -> Dict[str, Any]:
        """Process payment through PayPal."""
        try:
            # This would integrate with PayPal SDK
            # For now, return a placeholder response
            return {
                "success": True,
                "message": "PayPal payment processing - to be implemented",
                "amount": amount,
                "currency": currency
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def process_crypto_payment(
        self,
        amount: float,
        currency: str = "BTC",
        wallet_address: str = None
    ) -> Dict[str, Any]:
        """Process cryptocurrency payment."""
        try:
            # This would integrate with crypto payment gateways
            # For now, return a placeholder response
            return {
                "success": True,
                "message": "Cryptocurrency payment processing - to be implemented",
                "amount": amount,
                "currency": currency,
                "wallet_address": wallet_address
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def refund_payment(
        self,
        payment_intent_id: str,
        amount: Optional[float] = None,
        reason: str = "requested_by_customer"
    ) -> Dict[str, Any]:
        """Refund a payment."""
        try:
            refund_data = {
                "payment_intent": payment_intent_id,
                "reason": reason
            }
            
            if amount:
                refund_data["amount"] = int(amount * 100)
            
            refund = stripe.Refund.create(**refund_data)
            
            return {
                "success": True,
                "refund_id": refund.id,
                "status": refund.status,
                "amount": refund.amount / 100
            }
        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }


# Global payment processor instance
payment_processor = PaymentProcessor() 