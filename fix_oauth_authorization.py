#!/usr/bin/env python3
"""
OAuth Authorization Error Fix Script
This script helps fix common OAuth authorization errors.
"""

import os
import re
import webbrowser
from urllib.parse import quote

def print_header():
    """Print script header."""
    print("🔧 OAuth Authorization Error Fix")
    print("=" * 50)
    print("This script will help you fix OAuth authorization errors.")
    print()

def fix_google_oauth():
    """Fix Google OAuth authorization errors."""
    print("🔧 Google OAuth Authorization Fix")
    print("-" * 40)
    
    print("\n📋 Step-by-step fix:")
    print("1. Go to Google Cloud Console")
    print("2. Configure OAuth consent screen")
    print("3. Add test users")
    print("4. Update OAuth credentials")
    print("5. Test the fix")
    
    # Open Google Cloud Console
    print("\n🌐 Opening Google Cloud Console...")
    webbrowser.open("https://console.cloud.google.com/")
    
    print("\n📝 Follow these steps:")
    print("1. Select your project")
    print("2. Go to 'APIs & Services' > 'OAuth consent screen'")
    print("3. Choose 'External' user type")
    print("4. Fill in required fields:")
    print("   - App name: 'Ecommerce Platform'")
    print("   - User support email: your email")
    print("   - Developer contact information: your email")
    print("5. Add scopes: 'email', 'profile', 'openid'")
    print("6. Add test users: joshuawabulo56@gmail.com")
    print("7. Save and continue")
    
    input("\n⏸️  Press Enter when you've completed the OAuth consent screen setup...")
    
    # Open OAuth credentials
    print("\n🔑 Now let's update OAuth credentials:")
    webbrowser.open("https://console.cloud.google.com/apis/credentials")
    
    print("\n📝 Update OAuth 2.0 Client ID:")
    print("1. Click on your OAuth 2.0 Client ID")
    print("2. Update these settings:")
    print("   - Authorized JavaScript origins:")
    print("     * http://localhost:3003")
    print("     * http://127.0.0.1:3003")
    print("   - Authorized redirect URIs:")
    print("     * http://localhost:3003/auth/google/callback")
    print("     * http://127.0.0.1:3003/auth/google/callback")
    print("3. Save changes")
    
    input("\n⏸️  Press Enter when you've updated the OAuth credentials...")
    
    # Get new credentials
    print("\n🔑 Enter your updated credentials:")
    client_id = input("Google Client ID: ").strip()
    client_secret = input("Google Client Secret: ").strip()
    
    if client_id and client_secret:
        update_credentials(client_id, client_secret)
        print("\n✅ Credentials updated successfully!")
    else:
        print("\n❌ Please provide both Client ID and Client Secret.")

def update_credentials(client_id, client_secret):
    """Update OAuth credentials in all files."""
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
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            updated_content = re.sub(pattern, replacement, content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ Updated {file_path}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error updating {file_path}: {e}")
    
    print(f"\n✅ Updated {success_count}/{len(files_to_update)} files")

def test_oauth():
    """Test OAuth configuration."""
    print("\n🧪 Testing OAuth Configuration")
    print("-" * 40)
    
    print("1. Restart your backend server:")
    print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print()
    print("2. Restart your frontend server:")
    print("   cd frontend && npm run dev")
    print()
    print("3. Go to http://localhost:3003/login")
    print("4. Click the Google button")
    print("5. Sign in with joshuawabulo56@gmail.com")
    
    print("\n🔍 If you still get authorization errors:")
    print("- Check that joshuawabulo56@gmail.com is added as a test user")
    print("- Verify OAuth consent screen is published or in testing")
    print("- Ensure all redirect URIs are correct")
    print("- Check browser console for errors")

def show_troubleshooting():
    """Show troubleshooting steps."""
    print("\n🔍 Troubleshooting Authorization Errors")
    print("-" * 50)
    
    print("\n🚨 Common Issues and Solutions:")
    
    print("\n1. 'Access blocked' error:")
    print("   - Add your email as a test user in OAuth consent screen")
    print("   - Ensure app is in testing mode or published")
    print("   - Check that scopes include 'email' and 'profile'")
    
    print("\n2. 'Invalid client' error:")
    print("   - Verify Client ID is correct")
    print("   - Check that OAuth 2.0 credentials are properly configured")
    print("   - Ensure redirect URIs match exactly")
    
    print("\n3. 'Redirect URI mismatch' error:")
    print("   - Add both http://localhost:3003 and http://127.0.0.1:3003")
    print("   - Include both /auth/google/callback paths")
    print("   - Check for trailing slashes")
    
    print("\n4. 'Scope not allowed' error:")
    print("   - Add 'email', 'profile', 'openid' scopes in consent screen")
    print("   - Ensure scopes are properly configured")
    
    print("\n5. 'User not authorized' error:")
    print("   - Add joshuawabulo56@gmail.com as test user")
    print("   - Wait a few minutes for changes to propagate")
    print("   - Try clearing browser cache and cookies")

def main():
    """Main function."""
    print_header()
    
    while True:
        print("\n📋 Choose an option:")
        print("1. Fix Google OAuth Authorization Error")
        print("2. Test OAuth Configuration")
        print("3. Show Troubleshooting Steps")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            fix_google_oauth()
        elif choice == '2':
            test_oauth()
        elif choice == '3':
            show_troubleshooting()
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main() 