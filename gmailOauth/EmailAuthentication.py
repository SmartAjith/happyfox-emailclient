import os
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define the required scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def authenticate_gmail():
    """Authenticate the user and return the credentials."""
    creds = None
    token_path = 'token.json'
    creds_path = 'credentials.json'

    # Check if the token.json file exists to load the saved credentials
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logger.info("Token refreshed successfully.")
            except Exception as e:
                logger.error(f"Failed to refresh token: {e}")
                creds = None

        if not creds:
            if os.path.exists(creds_path):
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                creds = flow.run_local_server(port=8080, prompt='consent')
                # Save the credentials for the next run
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
                logger.info("Credentials saved successfully.")
            else:
                logger.error("Credentials file not found.")
                raise FileNotFoundError(f"{creds_path} not found")

    return creds