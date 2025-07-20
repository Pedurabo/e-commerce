# 🔧 Quick Fix for OAuth Authorization Error

## 🚨 **Problem**: Access blocked for joshuawabulo56@gmail.com

This error occurs because your email is not authorized to use the OAuth app. Here's how to fix it:

## ✅ **Step-by-Step Fix**

### **1. Go to Google Cloud Console**
- Visit: https://console.cloud.google.com/
- Select your project

### **2. Configure OAuth Consent Screen**
- Go to **APIs & Services** > **OAuth consent screen**
- Choose **External** user type
- Fill in required fields:
  - **App name**: Ecommerce Platform
  - **User support email**: your email
  - **Developer contact information**: your email
- Add these **scopes**:
  - `email`
  - `profile` 
  - `openid`
- **Save and continue**

### **3. Add Test Users**
- In the OAuth consent screen, go to **Test users** section
- Click **Add Users**
- Add: `joshuawabulo56@gmail.com`
- **Save**

### **4. Update OAuth Credentials**
- Go to **APIs & Services** > **Credentials**
- Click on your **OAuth 2.0 Client ID**
- Update **Authorized JavaScript origins**:
  ```
  http://localhost:3003
  http://127.0.0.1:3003
  ```
- Update **Authorized redirect URIs**:
  ```
  http://localhost:3003/auth/google/callback
  http://127.0.0.1:3003/auth/google/callback
  ```
- **Save**

### **5. Wait and Test**
- Wait 2-3 minutes for changes to propagate
- Clear browser cache and cookies
- Go to http://localhost:3003/login
- Try Google OAuth again

## 🔍 **Alternative Quick Fix**

If the above doesn't work, try this:

### **Option A: Publish the App**
- In OAuth consent screen, click **Publish App**
- This allows any user to access (not just test users)
- **Note**: This requires Google verification for production use

### **Option B: Use Different Email**
- Add a different Gmail address as test user
- Use that email for testing

### **Option C: Use Development Mode**
- Ensure app is in "Testing" mode
- Add multiple test users if needed

## 🚀 **Run the Fix Script**

Use the automated fix script:

```bash
python fix_oauth_authorization.py
```

This script will:
- Open Google Cloud Console automatically
- Guide you through the setup
- Update your credentials
- Test the configuration

## 🔧 **Manual Credential Update**

If you need to update credentials manually, replace these in your files:

**In `oauth_config.py`:**
```python
GOOGLE_CLIENT_ID = "your-actual-client-id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your-actual-client-secret"
```

**In `frontend/src/config/oauth.ts`:**
```typescript
GOOGLE: {
  CLIENT_ID: 'your-actual-client-id.apps.googleusercontent.com',
  // ...
}
```

**In `app/core/oauth.py`:**
```python
self.google_client_id = "your-actual-client-id.apps.googleusercontent.com"
self.google_client_secret = "your-actual-client-secret"
```

## 🧪 **Test the Fix**

1. **Restart servers**:
   ```bash
   # Backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Frontend (in another terminal)
   cd frontend
   npm run dev
   ```

2. **Test OAuth**:
   - Go to http://localhost:3003/login
   - Click Google button
   - Sign in with joshuawabulo56@gmail.com

## 🆘 **Still Having Issues?**

### **Check These Common Problems**:

1. **Test user not added**: Ensure joshuawabulo56@gmail.com is in test users list
2. **Wrong redirect URI**: Verify URIs match exactly
3. **App not in testing mode**: Ensure OAuth consent screen is configured
4. **Scopes missing**: Add email, profile, openid scopes
5. **Cache issues**: Clear browser cache and cookies

### **Debug Steps**:

1. **Check browser console** (F12) for errors
2. **Check backend logs** for OAuth errors
3. **Verify Google Cloud Console** settings
4. **Test with different browser**

## 📞 **Get Help**

If you're still experiencing issues:

1. Run the fix script: `python fix_oauth_authorization.py`
2. Check the troubleshooting guide: `OAUTH_TROUBLESHOOTING.md`
3. Verify all steps in this guide were followed
4. Check that your Google Cloud project is properly configured

## ✅ **Success Indicators**

When the fix works, you should see:
- Google OAuth popup opens
- No "Access blocked" error
- Successful sign-in with joshuawabulo56@gmail.com
- User created/logged in successfully
- Redirect to dashboard or home page 