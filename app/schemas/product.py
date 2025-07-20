"""
Product schemas for product and category management.
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CategoryBase(BaseModel):
    """Base category schema."""
    name: str
    description: Optional[str] = None
    slug: str
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    """Category creation schema."""
    pass


class CategoryUpdate(BaseModel):
    """Category update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    """Category response schema."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ProductImageBase(BaseModel):
    """Base product image schema."""
    image_url: str
    alt_text: Optional[str] = None
    is_primary: bool = False
    sort_order: int = 0


class ProductImageCreate(ProductImageBase):
    """Product image creation schema."""
    pass


class ProductImageResponse(ProductImageBase):
    """Product image response schema."""
    id: int
    product_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProductReviewBase(BaseModel):
    """Base product review schema."""
    rating: int
    title: Optional[str] = None
    comment: Optional[str] = None


class ProductReviewCreate(ProductReviewBase):
    """Product review creation schema."""
    pass


class ProductReviewResponse(ProductReviewBase):
    """Product review response schema."""
    id: int
    product_id: int
    user_id: int
    is_verified_purchase: bool
    is_approved: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    """Base product schema."""
    name: str
    description: Optional[str] = None
    short_description: Optional[str] = None
    sku: str
    price: float
    sale_price: Optional[float] = None
    cost_price: Optional[float] = None
    stock_quantity: int = 0
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    category_id: int
    is_featured: bool = False
    is_bestseller: bool = False
    tags: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class ProductCreate(ProductBase):
    """Product creation schema."""
    pass


class ProductUpdate(BaseModel):
    """Product update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = None
    sale_price: Optional[float] = None
    cost_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[str] = None
    is_featured: Optional[bool] = None
    is_bestseller: Optional[bool] = None
    tags: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None


class ProductResponse(ProductBase):
    """Product response schema."""
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Optional[CategoryResponse] = None
    images: List[ProductImageResponse] = []
    reviews: List[ProductReviewResponse] = []
    
    class Config:
        from_attributes = True


# Simple Product Response for frontend compatibility
class SimpleProductResponse(BaseModel):
    """Simple product response for frontend compatibility."""
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category: str = "Electronics"  # Default category
    stock: int = 0
    image_url: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, obj):
        """Custom from_orm method to handle category field."""
        # Get category name if available, otherwise use default
        category_name = "Electronics"  # Default category
        if hasattr(obj, 'category') and obj.category:
            if hasattr(obj.category, 'name'):
                category_name = obj.category.name
            elif isinstance(obj.category, str):
                category_name = obj.category
        
        data = {
            "id": obj.id,
            "name": obj.name,
            "description": obj.description,
            "price": obj.price,
            "category": category_name,
            "stock": obj.stock_quantity,
            "image_url": obj.image_url,
            "created_at": obj.created_at
        }
        return cls(**data)


class MLProductResponse(BaseModel):
    """ML-specific product response schema for frontend compatibility."""
    id: int
    name: str
    description: str
    short_description: str
    price: float
    original_price: float
    category: str
    subcategory: str
    brand: str
    rating: float
    reviews: int
    stock_quantity: int
    is_featured: bool
    is_bestseller: bool
    is_new: bool
    is_on_sale: bool
    discount_percentage: float
    tags: List[str]
    images: List[str]
    features: List[str]
    specifications: dict
    created_at: str
    updated_at: str 