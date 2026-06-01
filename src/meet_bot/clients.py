import os
import base64
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/meetings.space.created"]

def get_meet_client(token_file: str = "token.json", credentials_file: str = "credentials.json"):
    """Return an authorized Google Meet client (googleapiclient.discovery.Resource).

    This will read/write token_file and use credentials_file or GOOGLE_CREDENTIALS_BASE64 env var
    for the OAuth client configuration.
    """
    token_file = os.getenv("TOKEN_FILE", token_file)
    credentials_file = os.getenv("CREDENTIALS_FILE", credentials_file)
    
    creds = None
    
    # Check for token in environment variable first (for cloud deployment)
    token_base64 = os.getenv("TOKEN_JSON_BASE64")
    if token_base64:
        try:
            token_json = base64.b64decode(token_base64).decode('utf-8')
            # Parse and use the token data directly
            creds = Credentials.from_authorized_user_info(json.loads(token_json), SCOPES)
        except Exception as e:
            raise RuntimeError(f"Failed to decode TOKEN_JSON_BASE64: {e}")
    elif os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # In cloud environment, if we don't have valid creds and can't refresh, fail
            if token_base64:
                raise RuntimeError("Token in environment is invalid and cannot be refreshed")
            
            # Check if credentials are in environment variable (for cloud deployment)
            creds_base64 = os.getenv("GOOGLE_CREDENTIALS_BASE64")
            if creds_base64:
                raise RuntimeError("Cannot run OAuth flow in cloud environment - token.json is required")
            
            # Use credentials file (for local development only)
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open(token_file, "w") as f:
            f.write(creds.to_json())
    
    return build("meet", "v2", credentials=creds,
                 discoveryServiceUrl='https://meet.googleapis.com/$discovery/rest?version=v2')
