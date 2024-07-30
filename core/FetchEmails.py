import logging
from datetime import datetime
import re

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
        return extract_email_details(msg_id, message)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None    

def extract_email_details(msg_id, message):
    """Extract relevant email details from the message."""
    headers = message['payload']['headers']
    sender = next((header['value'] for header in headers if header['name'] == 'From'), None)
    recipient = next((header['value'] for header in headers if header['name'] == 'To'), None)
    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
    date_received_raw = next((header['value'] for header in headers if header['name'] == 'Date'), None)
    date_received = parse_date(date_received_raw)    
    snippet = message.get('snippet', '')
    
    return (msg_id, sender, recipient, subject, date_received, snippet)

def parse_date(date_str):
    """Parse the date string to the format MySQL DATETIME expects"""
    try:
        # Remove the extra text in parentheses
        date_str_clean = re.sub(r'\s+\(.*\)$', '', date_str)
        date_obj = datetime.strptime(date_str_clean, '%a, %d %b %Y %H:%M:%S %z')
        return date_obj.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        logger.error(f"Date parsing error: {e}")
        return None