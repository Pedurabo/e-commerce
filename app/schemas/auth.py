"""
Authentication schemas for login and token management.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    """User registration schema."""
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    username: str


class UserCreate(BaseModel):
    """User registration schema."""
    name: str
    email: EmailStr
    password: str
    user_type: str = "customer"  # "customer" or "admin"


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    name: str
    email: str
    user_type: str
    is_active: bool
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str
    user: UserResponse


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None


class TokenData(BaseModel):
    """Token data schema."""
    email: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None
    permissions: Optional[list] = None


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Password reset request schema."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation schema."""
    token: str
    new_password: str


class ChangePasswordRequest(BaseModel):
    """Change password request schema."""
    current_password: str
    new_password: str 