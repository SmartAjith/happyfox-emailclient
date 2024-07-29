import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate the user and return the credentials."""
    creds = None

    # Check if the token.json file exists to load the saved credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid or not creds.refresh_token:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Failed to refresh token: {e}")
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080, prompt='consent')  # Request offline access
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    return creds

if __name__ == '__main__':
    creds = authenticate_gmail()
    if creds:
        try:
            service = build('gmail', 'v1', credentials=creds)
            print("Gmail API service created successfully.")
        except Exception as e:
            print(f"Failed to create Gmail API service: {e}")
    else:
        print("Authentication failed.")