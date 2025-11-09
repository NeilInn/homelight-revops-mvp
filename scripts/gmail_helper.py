"""
Gmail API Helper - Create drafts in Gmail
"""
import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scope for creating drafts
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

def get_gmail_service():
    """
    Authenticate and return Gmail API service.
    First time: Opens browser for OAuth consent
    After that: Uses saved token
    """
    creds = None
    token_path = 'token.json'
    credentials_path = 'credentials.json'
    
    # Check if we already have a valid token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(
                    f"\n[ERROR] Missing {credentials_path}\n\n"
                    "Please follow setup instructions:\n"
                    "1. Go to https://console.cloud.google.com/\n"
                    "2. Create a new project (or select existing)\n"
                    "3. Enable Gmail API\n"
                    "4. Create OAuth 2.0 credentials\n"
                    "5. Download as 'credentials.json' and place in project root\n"
                )
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next time
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def create_draft(to_email, subject, body, sender_email=None):
    """
    Create a draft email in Gmail
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body (plain text)
        sender_email: Your email (optional, Gmail will use authenticated account)
    
    Returns:
        Draft ID if successful, None if failed
    """
    try:
        service = get_gmail_service()
        
        # Create the email message
        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = subject
        if sender_email:
            message['from'] = sender_email
        
        # Encode the message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        # Create draft
        draft_body = {'message': {'raw': raw_message}}
        draft = service.users().drafts().create(userId='me', body=draft_body).execute()
        
        draft_id = draft.get('id')
        return draft_id
        
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
    except FileNotFoundError as error:
        print(error)
        return None
    except Exception as error:
        print(f"Unexpected error: {error}")
        return None

def test_connection():
    """Test if Gmail API is properly configured"""
    try:
        service = get_gmail_service()
        # Try to get user profile to verify connection
        profile = service.users().getProfile(userId='me').execute()
        email = profile.get('emailAddress')
        print(f"[OK] Successfully connected to Gmail: {email}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to connect to Gmail: {e}")
        return False

if __name__ == "__main__":
    # Test the connection
    print("Testing Gmail API connection...")
    test_connection()

