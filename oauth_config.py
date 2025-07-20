"""
OAuth Configuration
Replace the placeholder values with your actual OAuth credentials.

For Google OAuth:
1. Go to https://console.cloud.google.com/
2. Create a new project or select existing one
3. Enable Google+ API
4. Go to Credentials > Create Credentials > OAuth 2.0 Client IDs
5. Set authorized redirect URIs to: http://localhost:3003/auth/google/callback
6. Copy the Client ID and Client Secret

For Facebook OAuth:
1. Go to https://developers.facebook.com/
2. Create a new app or select existing one
3. Add Facebook Login product
4. Go to Settings > Basic to get App ID and App Secret
5. Go to Facebook Login > Settings and add: http://localhost:3003/auth/facebook/callback
6. Copy the App ID and App Secret
"""

# Google OAuth Configuration
# TODO: Replace these with your actual Google OAuth credentials from Google Cloud Console
GOOGLE_CLIENT_ID = "your-actual-google-client-id.apps.googleusercontent.com"  # Replace with your actual Google Client ID
GOOGLE_CLIENT_SECRET = "your-actual-google-client-secret"  # Replace with your actual Google Client Secret

# Facebook OAuth Configuration
FACEBOOK_APP_ID = "your-facebook-app-id"  # Replace with your actual Facebook App ID
FACEBOOK_APP_SECRET = "your-facebook-app-secret"  # Replace with your actual Facebook App Secret

# Frontend OAuth URLs
FRONTEND_GOOGLE_CALLBACK = "http://localhost:3003/auth/google/callback"
FRONTEND_FACEBOOK_CALLBACK = "http://localhost:3003/auth/facebook/callback"

# Instructions for setup
SETUP_INSTRUCTIONS = """
SETUP INSTRUCTIONS:

1. Update the credentials above with your actual OAuth app credentials
2. Update the frontend configuration in frontend/src/config/oauth.ts
3. Update the backend configuration in app/core/oauth.py
4. Restart both frontend and backend servers

For production:
- Update redirect URIs to your production domain
- Store credentials in environment variables
- Use HTTPS for all OAuth callbacks
""" 