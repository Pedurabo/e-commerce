"""
Order endpoints for order management.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_orders():
    """Get all orders."""
    return {"message": "Orders endpoint - to be implemented"}


@router.post("/")
async def create_order():
    """Create a new order."""
    return {"message": "Create order - to be implemented"} 