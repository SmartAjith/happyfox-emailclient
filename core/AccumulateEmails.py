import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mysql.connector import Error
import logging
from googleapiclient.discovery import build
from FetchEmails import list_messages, get_message_details
from db.MysqlConnection import create_connection
from gmailOauth.EmailAuthentication import authenticate_gmail

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def insert_email(connection, email):
    """ Insert a new email into the emails table """
    if connection is not None:
        insert_query = """
        INSERT INTO emails (id, sender, recipient, subject, date_received, snippet)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor = connection.cursor()
        try:
            cursor.execute(insert_query, email)
            connection.commit()
            logger.info("Email inserted successfully")
        except Error as e:
            logger.info(f"Error: '{e}'")
    else:
        logging.info("Error! Cannot insert into the table without a connection.")

if __name__ == "__main__":
    try:
        creds = authenticate_gmail()
        if creds:
            service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail API service created successfully.")
            
            # Fetch list of emails from the inbox
            messages = list_messages(service, max_results=10)
            logger.info(f"Found {len(messages)} messages.")
            connection = create_connection("localhost", "root", "root", "happyFoxEmails")
            
            # Insert details of each message into Database
            for msg in messages:
                msg_details = get_message_details(service, 'me', msg['id'])
                insert_email(connection, msg_details)
        else:
            logger.error("Authentication failed.")
    except Exception as e:
        logger.error(f"Failed to authenticate or create Gmail API service: {e}")
