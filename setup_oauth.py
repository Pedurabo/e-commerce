#!/usr/bin/env python3
"""
OAuth Setup Script
This script helps you configure your OAuth credentials for Google and Facebook.
"""

import os
import re

def update_file_content(file_path, old_pattern, new_content):
    """Update file content with new OAuth credentials."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the placeholder with actual credentials
        updated_content = re.sub(old_pattern, new_content, content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Updated {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False

def setup_google_oauth():
    """Setup Google OAuth credentials."""
    print("\n🔧 Google OAuth Setup")
    print("=" * 50)
    
    print("\n📋 Instructions:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new project or select existing one")
    print("3. Enable Google+ API or Google Identity API")
    print("4. Go to APIs & Services > Credentials")
    print("5. Create OAuth 2.0 Client ID (Web application)")
    print("6. Set Authorized JavaScript origins: http://localhost:3003")
    print("7. Set Authorized redirect URIs: http://localhost:3003/auth/google/callback")
    print("8. Copy the Client ID and Client Secret")
    
    client_id = input("\n🔑 Enter your Google Client ID: ").strip()
    client_secret = input("🔐 Enter your Google Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Client ID and Client Secret are required!")
        return False
    
    # Update files
    files_to_update = [
        ('oauth_config.py', r'your-actual-google-client-id\.apps\.googleusercontent\.com', client_id),
        ('oauth_config.py', r'your-actual-google-client-secret', client_secret),
        ('frontend/src/config/oauth.ts', r'your-actual-google-client-id\.apps\.googleusercontent\.com', client_id),
        ('app/core/oauth.py', r'your-actual-google-client-id\.apps\.googleusercontent\.com', client_id),
        ('app/core/oauth.py', r'your-actual-google-client-secret', client_secret),
        ('frontend/src/contexts/AuthContext.tsx', r'your-actual-google-client-id\.apps\.googleusercontent\.com', client_id),
    ]
    
    success_count = 0
    for file_path, pattern, replacement in files_to_update:
        if update_file_content(file_path, pattern, replacement):
            success_count += 1
    
    print(f"\n✅ Updated {success_count}/{len(files_to_update)} files")
    return success_count == len(files_to_update)

def setup_facebook_oauth():
    """Setup Facebook OAuth credentials."""
    print("\n📘 Facebook OAuth Setup")
    print("=" * 50)
    
    print("\n📋 Instructions:")
    print("1. Go to https://developers.facebook.com/")
    print("2. Create a new app or select existing one")
    print("3. Add Facebook Login product")
    print("4. Go to Settings > Basic to get App ID and App Secret")
    print("5. Go to Facebook Login > Settings")
    print("6. Add Valid OAuth Redirect URIs: http://localhost:3003/auth/facebook/callback")
    
    app_id = input("\n🔑 Enter your Facebook App ID: ").strip()
    app_secret = input("🔐 Enter your Facebook App Secret: ").strip()
    
    if not app_id or not app_secret:
        print("❌ App ID and App Secret are required!")
        return False
    
    # Update files
    files_to_update = [
        ('oauth_config.py', r'your-facebook-app-id', app_id),
        ('oauth_config.py', r'your-facebook-app-secret', app_secret),
        ('frontend/src/config/oauth.ts', r'your-facebook-app-id', app_id),
        ('app/core/oauth.py', r'your-facebook-app-id', app_id),
        ('app/core/oauth.py', r'your-facebook-app-secret', app_secret),
        ('frontend/src/contexts/AuthContext.tsx', r'your-facebook-app-id', app_id),
    ]
    
    success_count = 0
    for file_path, pattern, replacement in files_to_update:
        if update_file_content(file_path, pattern, replacement):
            success_count += 1
    
    print(f"\n✅ Updated {success_count}/{len(files_to_update)} files")
    return success_count == len(files_to_update)

def main():
    """Main setup function."""
    print("🚀 OAuth Setup Script")
    print("=" * 50)
    print("This script will help you configure OAuth credentials for your ecommerce platform.")
    
    while True:
        print("\n📋 Choose an option:")
        print("1. Setup Google OAuth")
        print("2. Setup Facebook OAuth")
        print("3. Setup both")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            setup_google_oauth()
        elif choice == '2':
            setup_facebook_oauth()
        elif choice == '3':
            setup_google_oauth()
            setup_facebook_oauth()
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")
        
        if choice in ['1', '2', '3']:
            print("\n🔄 Next steps:")
            print("1. Restart your backend server")
            print("2. Restart your frontend server")
            print("3. Test OAuth login at http://localhost:3003/login")

if __name__ == "__main__":
    main() 