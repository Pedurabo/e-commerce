"""
Payment endpoints for payment processing.
"""

from fastapi import APIRouter

router = APIRouter()


@router.post("/stripe")
async def process_stripe_payment():
    """Process Stripe payment."""
    return {"message": "Stripe payment - to be implemented"}


@router.post("/paypal")
async def process_paypal_payment():
    """Process PayPal payment."""
    return {"message": "PayPal payment - to be implemented"}


@router.post("/crypto")
async def process_crypto_payment():
    """Process cryptocurrency payment."""
    return {"message": "Crypto payment - to be implemented"} 