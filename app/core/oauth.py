"""
OAuth service for Google and Facebook authentication.
"""

import httpx
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import create_access_token, create_refresh_token
from app.config import settings
from datetime import timedelta


class OAuthService:
    """Service for handling OAuth authentication."""
    
    def __init__(self):
        # Google OAuth configuration
        # TODO: Replace these with your actual Google OAuth credentials from Google Cloud Console
        self.google_client_id = "your-actual-google-client-id.apps.googleusercontent.com"  # Replace with actual
        self.google_client_secret = "your-actual-google-client-secret"  # Replace with actual
        
        # Facebook OAuth configuration
        self.facebook_app_id = "your-facebook-app-id"  # Replace with actual
        self.facebook_app_secret = "your-facebook-app-secret"  # Replace with actual
    
    async def authenticate_google(self, code: str, redirect_uri: str, db: Session) -> Optional[Dict[str, Any]]:
        """Authenticate user with Google OAuth."""
        try:
            # Exchange code for access token
            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                "client_id": self.google_client_id,
                "client_secret": self.google_client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            }
            
            async with httpx.AsyncClient() as client:
                token_response = await client.post(token_url, data=token_data)
                token_response.raise_for_status()
                token_info = token_response.json()
                
                # Get user info from Google
                user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
                headers = {"Authorization": f"Bearer {token_info['access_token']}"}
                user_response = await client.get(user_info_url, headers=headers)
                user_response.raise_for_status()
                user_info = user_response.json()
                
                # Find or create user
                user = self._get_or_create_user(
                    db=db,
                    email=user_info["email"],
                    first_name=user_info.get("given_name", ""),
                    last_name=user_info.get("family_name", ""),
                    provider="google",
                    provider_id=user_info["id"],
                    picture=user_info.get("picture")
                )
                
                if not user:
                    return None
                
                # Create tokens
                access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(
                    data={"sub": user.email, "type": "user"},
                    expires_delta=access_token_expires
                )
                
                refresh_token = create_refresh_token(
                    data={"sub": user.email, "type": "user"}
                )
                
                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                    "refresh_token": refresh_token,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": user.role,
                        "is_active": user.is_active,
                        "is_verified": user.is_verified,
                        "is_premium": user.is_premium,
                        "premium_expires_at": user.premium_expires_at,
                    }
                }
                
        except Exception as e:
            print(f"Google OAuth error: {e}")
            return None
    
    async def authenticate_facebook(self, code: str, redirect_uri: str, db: Session) -> Optional[Dict[str, Any]]:
        """Authenticate user with Facebook OAuth."""
        try:
            # Exchange code for access token
            token_url = "https://graph.facebook.com/v12.0/oauth/access_token"
            token_params = {
                "client_id": self.facebook_app_id,
                "client_secret": self.facebook_app_secret,
                "code": code,
                "redirect_uri": redirect_uri,
            }
            
            async with httpx.AsyncClient() as client:
                token_response = await client.get(token_url, params=token_params)
                token_response.raise_for_status()
                token_info = token_response.json()
                
                # Get user info from Facebook
                user_info_url = "https://graph.facebook.com/v12.0/me"
                user_params = {
                    "fields": "id,email,first_name,last_name,picture",
                    "access_token": token_info["access_token"]
                }
                user_response = await client.get(user_info_url, params=user_params)
                user_response.raise_for_status()
                user_info = user_response.json()
                
                # Find or create user
                user = self._get_or_create_user(
                    db=db,
                    email=user_info["email"],
                    first_name=user_info.get("first_name", ""),
                    last_name=user_info.get("last_name", ""),
                    provider="facebook",
                    provider_id=user_info["id"],
                    picture=user_info.get("picture", {}).get("data", {}).get("url") if user_info.get("picture") else None
                )
                
                if not user:
                    return None
                
                # Create tokens
                access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(
                    data={"sub": user.email, "type": "user"},
                    expires_delta=access_token_expires
                )
                
                refresh_token = create_refresh_token(
                    data={"sub": user.email, "type": "user"}
                )
                
                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                    "refresh_token": refresh_token,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": user.role,
                        "is_active": user.is_active,
                        "is_verified": user.is_verified,
                        "is_premium": user.is_premium,
                        "premium_expires_at": user.premium_expires_at,
                    }
                }
                
        except Exception as e:
            print(f"Facebook OAuth error: {e}")
            return None
    
    def _get_or_create_user(
        self, 
        db: Session, 
        email: str, 
        first_name: str, 
        last_name: str, 
        provider: str, 
        provider_id: str,
        picture: Optional[str] = None
    ) -> Optional[User]:
        """Get existing user or create new one from OAuth data."""
        # Check if user already exists
        user = db.query(User).filter(User.email == email).first()
        
        if user:
            # Update user info if needed
            if not user.first_name and first_name:
                user.first_name = first_name
            if not user.last_name and last_name:
                user.last_name = last_name
            if not user.is_verified:
                user.is_verified = True  # OAuth users are verified
            db.commit()
            return user
        
        # Create new user
        try:
            username = email.split('@')[0]  # Use email prefix as username
            # Ensure username is unique
            base_username = username
            counter = 1
            while db.query(User).filter(User.username == username).first():
                username = f"{base_username}{counter}"
                counter += 1
            
            new_user = User(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                is_verified=True,  # OAuth users are verified
                is_active=True,
                role="customer"
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
            
        except Exception as e:
            print(f"Error creating user: {e}")
            db.rollback()
            return None


# Create OAuth service instance
oauth_service = OAuthService() 