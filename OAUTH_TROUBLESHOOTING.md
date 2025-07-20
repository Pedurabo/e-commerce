# OAuth Authentication Troubleshooting Guide

## 🚨 Common OAuth Errors and Solutions

### **Error: "The OAuth client was not found"**

**Problem**: Using placeholder credentials instead of real Google OAuth credentials.

**Solution**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create OAuth 2.0 credentials
3. Replace placeholder credentials in all configuration files
4. Use the setup script: `python setup_oauth.py`

### **Error: "Invalid redirect URI"**

**Problem**: Redirect URI doesn't match what's configured in Google/Facebook console.

**Solution**:
1. **Google Console**: Add `http://localhost:3003/auth/google/callback` to Authorized redirect URIs
2. **Facebook Console**: Add `http://localhost:3003/auth/facebook/callback` to Valid OAuth Redirect URIs
3. Ensure no trailing slashes or protocol mismatches

### **Error: "Client ID not found"**

**Problem**: Client ID is incorrect or OAuth app not properly configured.

**Solution**:
1. Verify Client ID is copied correctly from Google Cloud Console
2. Ensure OAuth consent screen is configured
3. Check that the API is enabled (Google+ API or Google Identity API)

### **Error: "Network error during OAuth"**

**Problem**: Backend or frontend servers not running.

**Solution**:
1. Start backend: `python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
2. Start frontend: `cd frontend && npm run dev`
3. Verify both servers are running on correct ports

### **Error: "Popup blocked"**

**Problem**: Browser blocking popup windows.

**Solution**:
1. Allow popups for `localhost:3003`
2. Check browser security settings
3. Try a different browser

## 🔧 Quick Fix Commands

### **1. Run Setup Script**
```bash
python setup_oauth.py
```

### **2. Restart Servers**
```bash
# Backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (in another terminal)
cd frontend
npm run dev
```

### **3. Test OAuth Endpoints**
```bash
# Test backend health
curl http://localhost:8000/health

# Test OAuth endpoints (should return 422 for missing credentials)
curl -X POST http://localhost:8000/api/v1/auth/google
curl -X POST http://localhost:8000/api/v1/auth/facebook
```

## 📋 Configuration Checklist

### **Google OAuth Setup**
- [ ] Created Google Cloud project
- [ ] Enabled Google+ API or Google Identity API
- [ ] Created OAuth 2.0 Client ID (Web application)
- [ ] Set Authorized JavaScript origins: `http://localhost:3003`
- [ ] Set Authorized redirect URIs: `http://localhost:3003/auth/google/callback`
- [ ] Updated all configuration files with real credentials
- [ ] Restarted both servers

### **Facebook OAuth Setup**
- [ ] Created Facebook app
- [ ] Added Facebook Login product
- [ ] Set Valid OAuth Redirect URIs: `http://localhost:3003/auth/facebook/callback`
- [ ] Updated all configuration files with real credentials
- [ ] Restarted both servers

## 🔍 Debug Steps

### **1. Check Browser Console**
- Open Developer Tools (F12)
- Go to Console tab
- Look for JavaScript errors
- Check Network tab for failed requests

### **2. Check Backend Logs**
- Look for Python errors in terminal
- Check for OAuth-related error messages
- Verify database connections

### **3. Test OAuth URLs**
- Test Google OAuth URL manually
- Verify redirect URIs are correct
- Check for typos in credentials

### **4. Verify File Updates**
- Check that all configuration files were updated
- Ensure no placeholder values remain
- Verify file permissions

## 🆘 Still Having Issues?

### **1. Use the Setup Script**
```bash
python setup_oauth.py
```

### **2. Manual Configuration**
If the script doesn't work, manually update these files:
- `oauth_config.py`
- `frontend/src/config/oauth.ts`
- `app/core/oauth.py`
- `frontend/src/contexts/AuthContext.tsx`

### **3. Check File Permissions**
Ensure you have write permissions to all configuration files.

### **4. Verify Network**
- Check if localhost is accessible
- Ensure no firewall blocking ports 8000 and 3003
- Try disabling antivirus temporarily

### **5. Test with Different Browser**
- Try Chrome, Firefox, or Edge
- Clear browser cache and cookies
- Disable browser extensions temporarily

## 📞 Getting Help

If you're still experiencing issues:

1. **Check the logs**: Look at both frontend and backend console output
2. **Verify credentials**: Double-check all OAuth credentials
3. **Test step by step**: Follow the setup guide exactly
4. **Use the setup script**: It automates the configuration process

## 🎯 Success Indicators

When OAuth is working correctly, you should see:

1. **Google OAuth popup opens** when clicking Google button
2. **Facebook OAuth popup opens** when clicking Facebook button
3. **Successful authentication** and user creation/login
4. **Welcome message** with user's name
5. **Redirect to dashboard** or home page

## 🔄 Next Steps After Fix

Once OAuth is working:

1. **Test user creation**: Try logging in with a new Google/Facebook account
2. **Test existing users**: Try logging in with accounts that already exist
3. **Customize user experience**: Add profile pictures, additional fields
4. **Add more providers**: Implement Twitter, GitHub, etc.
5. **Production deployment**: Update URLs and security settings 