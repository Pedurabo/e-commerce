from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models import Cart, CartItem, Product, User
from app.schemas.cart import CartItemCreate, CartItemResponse, CartResponse
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=CartResponse)
async def get_cart(
    db: Session = Depends(get_db)
):
    """Get user's cart with all items."""
    cart = db.query(Cart).filter(Cart.user_id == 1).first()
    
    if not cart:
        # Create new cart if it doesn't exist (Demo mode - use user_id 1)
        cart = Cart(user_id=1, created_at=datetime.utcnow())
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    # Get cart items with product details
    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    
    total = 0
    items = []
    
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            item_total = product.price * item.quantity
            total += item_total
            
            items.append({
                "id": item.id,
                "product_id": item.product_id,
                "product_name": product.name,
                "product_price": product.price,
                "quantity": item.quantity,
                "total": item_total
            })
    
    return {
        "cart_id": cart.id,
        "user_id": cart.user_id,
        "items": items,
        "total": total,
        "item_count": len(items)
    }

@router.post("/add", response_model=CartItemResponse)
async def add_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db)
):
    """Add product to cart (Demo mode - no auth required)."""
    """Add product to cart."""
    # Verify product exists
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check stock availability
    if product.stock_quantity < item.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock"
        )
    
    # Get or create cart (Demo mode - use user_id 1)
    cart = db.query(Cart).filter(Cart.user_id == 1).first()
    if not cart:
        cart = Cart(user_id=1, created_at=datetime.utcnow())
        db.add(cart)
        db.commit()
        db.refresh(cart)
    
    # Check if item already exists in cart
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item.product_id
    ).first()
    
    if existing_item:
        # Update quantity
        new_quantity = existing_item.quantity + item.quantity
        if product.stock_quantity < new_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient stock for requested quantity"
            )
        
        existing_item.quantity = new_quantity
        existing_item.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_item)
        
        return {
            "id": existing_item.id,
            "product_id": existing_item.product_id,
            "quantity": existing_item.quantity,
            "updated_at": existing_item.updated_at
        }
    else:
        # Add new item
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item.product_id,
            quantity=item.quantity,
            created_at=datetime.utcnow()
        )
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        
        return {
            "id": cart_item.id,
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity,
            "created_at": cart_item.created_at
        }

@router.put("/items/{item_id}", response_model=CartItemResponse)
async def update_cart_item(
    item_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):
    """Update cart item quantity."""
    if quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantity must be greater than 0"
        )
    
    # Get cart item (Demo mode - use user_id 1)
    cart_item = db.query(CartItem).join(Cart).filter(
        CartItem.id == item_id,
        Cart.user_id == 1
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    # Check stock availability
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if product and product.stock_quantity < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock"
        )
    
    # Update quantity
    cart_item.quantity = quantity
    cart_item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(cart_item)
    
    return {
        "id": cart_item.id,
        "product_id": cart_item.product_id,
        "quantity": cart_item.quantity,
        "updated_at": cart_item.updated_at
    }

@router.delete("/items/{item_id}")
async def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Remove item from cart."""
    cart_item = db.query(CartItem).join(Cart).filter(
        CartItem.id == item_id,
        Cart.user_id == 1
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    db.delete(cart_item)
    db.commit()
    
    return {"message": "Item removed from cart"}

@router.delete("/clear")
async def clear_cart(
    db: Session = Depends(get_db)
):
    """Clear all items from cart (Demo mode)."""
    cart = db.query(Cart).filter(Cart.user_id == 1).first()
    
    if cart:
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        db.commit()
    
    return {"message": "Cart cleared"}

@router.get("/count")
async def get_cart_count(
    db: Session = Depends(get_db)
):
    """Get total number of items in cart (Demo mode)."""
    cart = db.query(Cart).filter(Cart.user_id == 1).first()
    
    if not cart:
        return {"count": 0}
    
    count = db.query(CartItem).filter(CartItem.cart_id == cart.id).count()
    return {"count": count}

@router.post("/checkout")
async def checkout(
    db: Session = Depends(get_db)
):
    """Process cart checkout (Demo mode)."""
    cart = db.query(Cart).filter(Cart.user_id == 1).first()
    
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # Validate stock and calculate total
    total = 0
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product {item.product_id} not found"
            )
        
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for {product.name}"
            )
        
        total += product.price * item.quantity
    
    # In a real implementation, you would:
    # 1. Create an order
    # 2. Process payment
    # 3. Update product stock
    # 4. Clear cart
    # 5. Send confirmation email
    
    # For now, just clear the cart
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    
    return {
        "message": "Checkout successful",
        "total": total,
        "order_id": f"ORD-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    } 