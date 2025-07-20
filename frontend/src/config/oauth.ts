// OAuth Configuration
export const OAUTH_CONFIG = {
  // Google OAuth Configuration
  GOOGLE: {
    CLIENT_ID: 'your-actual-google-client-id.apps.googleusercontent.com', // TODO: Replace with your actual Google Client ID from Google Cloud Console
    REDIRECT_URI: 'http://localhost:3003/auth/google/callback',
    SCOPE: 'email profile',
  },
  
  // Facebook OAuth Configuration
  FACEBOOK: {
    APP_ID: 'your-facebook-app-id', // Replace with your actual Facebook App ID
    REDIRECT_URI: 'http://localhost:3003/auth/facebook/callback',
    SCOPE: 'email public_profile',
  },
  
  // Backend API endpoints
  API: {
    GOOGLE_AUTH: 'http://localhost:8000/api/v1/auth/google',
    FACEBOOK_AUTH: 'http://localhost:8000/api/v1/auth/facebook',
  }
}

// OAuth URLs
export const OAUTH_URLS = {
  GOOGLE: `https://accounts.google.com/o/oauth2/v2/auth?client_id=${OAUTH_CONFIG.GOOGLE.CLIENT_ID}&redirect_uri=${encodeURIComponent(OAUTH_CONFIG.GOOGLE.REDIRECT_URI)}&scope=${encodeURIComponent(OAUTH_CONFIG.GOOGLE.SCOPE)}&response_type=code&access_type=offline&prompt=consent`,
  FACEBOOK: `https://www.facebook.com/v12.0/dialog/oauth?client_id=${OAUTH_CONFIG.FACEBOOK.APP_ID}&redirect_uri=${encodeURIComponent(OAUTH_CONFIG.FACEBOOK.REDIRECT_URI)}&scope=${encodeURIComponent(OAUTH_CONFIG.FACEBOOK.SCOPE)}&response_type=code`,
}

// OAuth callback handler
export const handleOAuthCallback = async (provider: 'google' | 'facebook', code: string) => {
  try {
    const apiEndpoint = provider === 'google' ? OAUTH_CONFIG.API.GOOGLE_AUTH : OAUTH_CONFIG.API.FACEBOOK_AUTH
    const redirectUri = provider === 'google' ? OAUTH_CONFIG.GOOGLE.REDIRECT_URI : OAUTH_CONFIG.FACEBOOK.REDIRECT_URI
    
    const response = await fetch(apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code, redirect_uri: redirectUri }),
    })

    if (response.ok) {
      const data = await response.json()
      return { success: true, data }
    } else {
      const error = await response.json()
      return { success: false, error: error.detail || 'OAuth authentication failed' }
    }
  } catch (error) {
    console.error(`${provider} OAuth error:`, error)
    return { success: false, error: 'Network error during OAuth authentication' }
  }
} 