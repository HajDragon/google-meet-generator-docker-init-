"""Generate token.json by authorizing with Google."""
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/meetings.space.created"]

def main():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    
    with open('token.json', 'w') as f:
        f.write(creds.to_json())
    
    print("✅ token.json generated successfully!")

if __name__ == "__main__":
    main()
