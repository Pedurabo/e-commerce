#!/usr/bin/env python3
"""
OAuth Credentials Update Script
This script helps you update your OAuth credentials with real values.
"""

import os
import re

def update_file(file_path, old_pattern, new_content):
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

def main():
    print("🔧 OAuth Credentials Update")
    print("=" * 40)
    print("This script will help you update your OAuth credentials.")
    print()
    
    # Get user input
    client_id = input("Enter your Google Client ID (ends with .apps.googleusercontent.com): ").strip()
    client_secret = input("Enter your Google Client Secret: ").strip()
    
    if not client_id or not client_secret:
        print("❌ Both Client ID and Client Secret are required!")
        return
    
    print("\n🔄 Updating files...")
    
    # Update oauth_config.py
    update_file(
        'oauth_config.py',
        r'GOOGLE_CLIENT_ID = "your-actual-google-client-id\.apps\.googleusercontent\.com"',
        f'GOOGLE_CLIENT_ID = "{client_id}"'
    )
    
    update_file(
        'oauth_config.py',
        r'GOOGLE_CLIENT_SECRET = "your-actual-google-client-secret"',
        f'GOOGLE_CLIENT_SECRET = "{client_secret}"'
    )
    
    # Update frontend/src/config/oauth.ts
    update_file(
        'frontend/src/config/oauth.ts',
        r"CLIENT_ID: 'your-actual-google-client-id\.apps\.googleusercontent\.com'",
        f"CLIENT_ID: '{client_id}'"
    )
    
    # Update app/core/oauth.py
    update_file(
        'app/core/oauth.py',
        r'self\.google_client_id = "your-actual-google-client-id\.apps\.googleusercontent\.com"',
        f'self.google_client_id = "{client_id}"'
    )
    
    update_file(
        'app/core/oauth.py',
        r'self\.google_client_secret = "your-actual-google-client-secret"',
        f'self.google_client_secret = "{client_secret}"'
    )
    
    # Update frontend/src/contexts/AuthContext.tsx
    update_file(
        'frontend/src/contexts/AuthContext.tsx',
        r'client_id=your-actual-google-client-id\.apps\.googleusercontent\.com',
        f'client_id={client_id}'
    )
    
    print("\n✅ Credentials updated successfully!")
    print("\n📋 Next steps:")
    print("1. Make sure your Google OAuth app is configured correctly")
    print("2. Add your email as a test user in Google Cloud Console")
    print("3. Restart your servers")
    print("4. Test OAuth login at http://localhost:3003/login")

if __name__ == "__main__":
    main() 