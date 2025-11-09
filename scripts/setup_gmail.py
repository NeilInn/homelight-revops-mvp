"""
Quick setup script for Gmail API
Run this after creating credentials.json
"""
import os
import sys

def check_credentials():
    """Check if credentials.json exists"""
    if not os.path.exists('credentials.json'):
        print("[X] credentials.json not found!")
        print("\n[SETUP] To get credentials.json:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create/select a project")
        print("3. Enable Gmail API")
        print("4. Create OAuth 2.0 credentials (Desktop app)")
        print("5. Download as 'credentials.json'")
        print("6. Place in: homelight-revops-mvp/credentials.json")
        print("\n[GUIDE] Full guide: docs/gmail_setup_guide.md\n")
        return False
    print("[OK] credentials.json found")
    return True

def check_packages():
    """Check if required packages are installed"""
    try:
        import google.auth
        import google_auth_oauthlib
        import googleapiclient
        print("[OK] Google API packages installed")
        return True
    except ImportError:
        print("[X] Google API packages not installed")
        print("\n[INSTALL] Run: pip install -r requirements.txt\n")
        return False

def test_connection():
    """Test Gmail API connection"""
    print("\n[AUTH] Testing Gmail API connection...")
    print("(A browser window will open for authentication)")
    
    try:
        from gmail_helper import test_connection
        success = test_connection()
        
        if success:
            print("\n[SUCCESS] Setup complete!")
            print("[OK] You can now create Gmail drafts from the dashboard")
            print("\n[RUN] Run: streamlit run app/streamlit_app.py")
        else:
            print("\n[ERROR] Connection failed")
            print("[HELP] See troubleshooting in: docs/gmail_setup_guide.md")
        
        return success
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False

def main():
    print("="*60)
    print("Gmail API Setup for RevOps MVP")
    print("="*60)
    print()
    
    # Check credentials
    if not check_credentials():
        sys.exit(1)
    
    # Check packages
    if not check_packages():
        sys.exit(1)
    
    # Test connection
    test_connection()

if __name__ == "__main__":
    main()

