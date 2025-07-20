# 🚨 Quick Fix for OAuth Client Error

## **Error**: "The OAuth client was not found" / "Error 401: invalid_client"

This error occurs because you're using placeholder credentials instead of real Google OAuth credentials.

## ✅ **Immediate Solution**

### **Step 1: Get Real Google OAuth Credentials**

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project** (or select existing)
3. **Enable APIs**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API" or "Google Identity API"
   - Click "Enable"

4. **Create OAuth 2.0 Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Web application"
   - **Name**: "Ecommerce Platform"
   - **Authorized JavaScript origins**: `http://localhost:3003`
   - **Authorized redirect URIs**: `http://localhost:3003/auth/google/callback`
   - Click "Create"

5. **Copy your credentials**:
   - You'll get a **Client ID** and **Client Secret**
   - Copy these values

### **Step 2: Update Your Configuration**

Replace the placeholder credentials in these files:

**File: `oauth_config.py`**
```python
GOOGLE_CLIENT_ID = "YOUR_ACTUAL_CLIENT_ID.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "YOUR_ACTUAL_CLIENT_SECRET"
```

**File: `frontend/src/config/oauth.ts`**
```typescript
GOOGLE: {
  CLIENT_ID: 'YOUR_ACTUAL_CLIENT_ID.apps.googleusercontent.com',
  REDIRECT_URI: 'http://localhost:3003/auth/google/callback',
  SCOPE: 'email profile',
},
```

**File: `app/core/oauth.py`**
```python
self.google_client_id = "YOUR_ACTUAL_CLIENT_ID.apps.googleusercontent.com"
self.google_client_secret = "YOUR_ACTUAL_CLIENT_SECRET"
```

**File: `frontend/src/contexts/AuthContext.tsx`**
```typescript
`https://accounts.google.com/o/oauth2/v2/auth?client_id=YOUR_ACTUAL_CLIENT_ID.apps.googleusercontent.com&redirect_uri=${encodeURIComponent('http://localhost:3003/auth/google/callback')}&scope=${encodeURIComponent('email profile')}&response_type=code&access_type=offline&prompt=consent`
```

### **Step 3: Configure OAuth Consent Screen**

1. Go to "APIs & Services" > "OAuth consent screen"
2. Choose "External" user type
3. Fill in required fields:
   - **App name**: Ecommerce Platform
   - **User support email**: your email
   - **Developer contact information**: your email
4. Add scopes: `email`, `profile`, `openid`
5. **Add test users**: Add `joshuawabulo56@gmail.com`
6. Save and continue

### **Step 4: Restart Servers**

```bash
# Stop current servers (Ctrl+C)
# Then restart:

# Backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (in another terminal)
cd frontend
npm run dev
```

### **Step 5: Test OAuth**

1. Go to http://localhost:3003/login
2. Click "Sign in with Google"
3. Sign in with `joshuawabulo56@gmail.com`

## 🔍 **Troubleshooting**

- **Still getting errors?** Make sure you've replaced ALL placeholder credentials
- **Redirect URI error?** Double-check the redirect URI matches exactly
- **Test user error?** Make sure your email is added as a test user
- **Port conflicts?** Make sure no other apps are using port 8000 or 3003

## 📞 **Need Help?**

If you're still having issues, check:
1. Google Cloud Console for any error messages
2. Browser console for JavaScript errors
3. Backend logs for Python errors 