import os
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

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

def list_messages(service, user_id='me', max_results=100):
    """List up to max_results messages of the user's mailbox."""
    try:
        response = service.users().messages().list(userId=user_id, maxResults=max_results).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        return messages
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return []

def get_message_details(service, user_id, msg_id):
    """Get details of a single message."""
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        return message
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    try:
        creds = authenticate_gmail()
        if creds:
            service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail API service created successfully.")
            
            # Fetch and list up to 100 emails from the inbox without any query
            messages = list_messages(service, max_results=100)
            logger.info(f"Found {len(messages)} messages.")
            
            # Print details of each message
            for msg in messages:
                msg_details = get_message_details(service, 'me', msg['id'])
                if msg_details:
                    logger.info(f"Message snippet: {msg_details['snippet']}")
        else:
            logger.error("Authentication failed.")
    except Exception as e:
        logger.error(f"Failed to authenticate or create Gmail API service: {e}")
