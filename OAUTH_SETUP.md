# OAuth Authentication Setup Guide

This guide will help you set up Google and Facebook OAuth authentication for your ecommerce platform.

## 🚀 Quick Start

1. **Update OAuth Credentials**: Edit `oauth_config.py` with your actual credentials
2. **Update Frontend Config**: Edit `frontend/src/config/oauth.ts` with your credentials
3. **Update Backend Config**: Edit `app/core/oauth.py` with your credentials
4. **Restart Servers**: Restart both frontend and backend servers

## 📋 Prerequisites

- Google Cloud Console account
- Facebook Developer account
- Both frontend and backend servers running

## 🔧 Google OAuth Setup

### Step 1: Create Google OAuth App

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google+ API** (or Google Identity API)
4. Go to **Credentials** > **Create Credentials** > **OAuth 2.0 Client IDs**
5. Choose **Web application** as the application type
6. Set the following:
   - **Name**: Your app name (e.g., "Ecommerce Platform")
   - **Authorized JavaScript origins**: `http://localhost:3003`
   - **Authorized redirect URIs**: `http://localhost:3003/auth/google/callback`
7. Click **Create**
8. Copy the **Client ID** and **Client Secret**

### Step 2: Update Configuration

Update the following files with your Google credentials:

**Backend** (`app/core/oauth.py`):
```python
self.google_client_id = "your-actual-google-client-id.apps.googleusercontent.com"
self.google_client_secret = "your-actual-google-client-secret"
```

**Frontend** (`frontend/src/config/oauth.ts`):
```typescript
GOOGLE: {
  CLIENT_ID: 'your-actual-google-client-id.apps.googleusercontent.com',
  REDIRECT_URI: 'http://localhost:3003/auth/google/callback',
  SCOPE: 'email profile',
},
```

## 📘 Facebook OAuth Setup

### Step 1: Create Facebook App

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Click **Create App** or select an existing app
3. Choose **Consumer** as the app type
4. Fill in the app details and create the app
5. Add the **Facebook Login** product to your app
6. Go to **Facebook Login** > **Settings**
7. Add the following to **Valid OAuth Redirect URIs**:
   - `http://localhost:3003/auth/facebook/callback`
8. Go to **Settings** > **Basic** to get your **App ID** and **App Secret**

### Step 2: Update Configuration

Update the following files with your Facebook credentials:

**Backend** (`app/core/oauth.py`):
```python
self.facebook_app_id = "your-actual-facebook-app-id"
self.facebook_app_secret = "your-actual-facebook-app-secret"
```

**Frontend** (`frontend/src/config/oauth.ts`):
```typescript
FACEBOOK: {
  APP_ID: 'your-actual-facebook-app-id',
  REDIRECT_URI: 'http://localhost:3003/auth/facebook/callback',
  SCOPE: 'email public_profile',
},
```

## 🔄 Testing OAuth

1. **Start both servers**:
   ```bash
   # Backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Frontend
   cd frontend
   npm run dev
   ```

2. **Navigate to login page**: `http://localhost:3003/login`

3. **Test OAuth buttons**: Click on Google or Facebook buttons

4. **Check browser console** for any errors

## 🛠️ Troubleshooting

### Common Issues

1. **"Invalid redirect URI" error**:
   - Ensure redirect URIs match exactly in both Google/Facebook console and your code
   - Check for trailing slashes or protocol mismatches

2. **"Client ID not found" error**:
   - Verify your Client ID is correct
   - Ensure the OAuth app is properly configured

3. **"Network error" during OAuth**:
   - Check if both servers are running
   - Verify CORS settings allow localhost:3003

4. **Popup blocked**:
   - Allow popups for localhost:3003
   - Check browser security settings

### Debug Steps

1. **Check browser console** for JavaScript errors
2. **Check backend logs** for Python errors
3. **Verify OAuth URLs** are correct
4. **Test with different browsers**

## 🔒 Security Considerations

### For Development
- Use localhost for testing
- Keep credentials in code (not recommended for production)

### For Production
- Store credentials in environment variables
- Use HTTPS for all OAuth callbacks
- Update redirect URIs to your production domain
- Implement proper session management
- Add rate limiting to OAuth endpoints

## 📁 File Structure

```
ecommerce/
├── oauth_config.py              # OAuth credentials configuration
├── app/
│   ├── core/
│   │   └── oauth.py            # OAuth service implementation
│   ├── schemas/
│   │   └── oauth.py            # OAuth request/response schemas
│   └── api/v1/endpoints/
│       └── auth.py             # OAuth endpoints
└── frontend/
    ├── src/
    │   ├── config/
    │   │   └── oauth.ts        # Frontend OAuth configuration
    │   ├── contexts/
    │   │   └── AuthContext.tsx # OAuth authentication logic
    │   └── pages/
    │       ├── LoginPage.tsx   # OAuth login buttons
    │       └── OAuthCallbackPage.tsx # OAuth callback handler
    └── main.tsx                # OAuth callback routes
```

## 🎯 Features Implemented

- ✅ Google OAuth authentication
- ✅ Facebook OAuth authentication
- ✅ Automatic user creation for new OAuth users
- ✅ User profile synchronization
- ✅ Secure token generation
- ✅ Popup-based OAuth flow
- ✅ Error handling and user feedback
- ✅ Responsive UI with hover effects

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all credentials are correct
3. Ensure both servers are running
4. Check browser console and backend logs
5. Test with different browsers

## 🔄 Next Steps

After successful OAuth setup:

1. **Customize user experience**: Add profile picture display
2. **Add more providers**: Implement Twitter, GitHub, etc.
3. **Enhance security**: Add CSRF protection, rate limiting
4. **Improve UX**: Add loading states, better error messages
5. **Production deployment**: Update URLs and security settings 