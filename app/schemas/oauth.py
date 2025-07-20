"""
OAuth schemas for Google and Facebook authentication.
"""

from pydantic import BaseModel
from typing import Optional


class OAuthRequest(BaseModel):
    """Base OAuth request schema."""
    code: str
    redirect_uri: str


class GoogleOAuthRequest(OAuthRequest):
    """Google OAuth request schema."""
    pass


class FacebookOAuthRequest(OAuthRequest):
    """Facebook OAuth request schema."""
    pass


class OAuthUserInfo(BaseModel):
    """OAuth user information schema."""
    email: str
    first_name: str
    last_name: str
    picture: Optional[str] = None
    provider: str  # 'google' or 'facebook'
    provider_id: str


class OAuthResponse(BaseModel):
    """OAuth response schema."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    user: OAuthUserInfo 