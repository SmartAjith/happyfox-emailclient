import logging
from googleapiclient.discovery import build
from EmailAuthentication import authenticate_gmail

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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