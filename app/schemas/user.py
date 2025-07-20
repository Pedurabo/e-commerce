"""
User schemas for customer and admin management.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    phone: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema."""
    password: str


class UserUpdate(BaseModel):
    """User update schema."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """User response schema."""
    id: int
    is_active: bool
    is_verified: bool
    role: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AdminBase(BaseModel):
    """Base admin schema."""
    email: EmailStr
    username: str
    first_name: str
    last_name: str


class AdminCreate(AdminBase):
    """Admin creation schema."""
    password: str
    is_super_admin: bool = False
    permissions: Optional[list] = None


class AdminUpdate(BaseModel):
    """Admin update schema."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_super_admin: Optional[bool] = None
    permissions: Optional[list] = None
    is_active: Optional[bool] = None


class AdminResponse(AdminBase):
    """Admin response schema."""
    id: int
    is_super_admin: bool
    permissions: Optional[list] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True 