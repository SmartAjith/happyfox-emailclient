import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
import logging
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from gmailOauth.EmailAuthentication import authenticate_gmail
from db.MysqlConnection import create_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
db = create_connection("localhost", "root", "root", "happyFoxEmails")
cursor = db.cursor(dictionary=True)

# Load rules from JSON file
with open('resources/rules.json', 'r') as file:
    rules = json.load(file)

creds = authenticate_gmail()
service = build('gmail', 'v1', credentials=creds)

def apply_rules():
    for rule in rules:
        conditions = rule['conditions']
        rule_predicate = rule['predicate']
        actions = rule['actions']
        
        query = "SELECT * FROM emails WHERE "
        condition_clauses = []
        values = []
        
        for condition in conditions:
            field = condition['field']
            predicate = condition['predicate']
            value = condition['value']
            
            if field == 'From':
                if predicate == 'contains':
                    condition_clauses.append("sender LIKE %s")
                    values.append(f"%{value}%")
                elif predicate == 'equals':
                    condition_clauses.append("sender = %s")
                    values.append(value)
                # Add other predicates as needed
            elif field == 'Subject':
                if predicate == 'contains':
                    condition_clauses.append("subject LIKE %s")
                    values.append(f"%{value}%")
                elif predicate == 'equals':
                    condition_clauses.append("subject = %s")
                    values.append(value)
            elif field == 'Date Received':
                if predicate == 'less_than_days':
                    target_date = datetime.now() - timedelta(days=int(value))
                    condition_clauses.append("date_received > %s")
                    values.append(target_date)
                elif predicate == 'greater_than_days':
                    target_date = datetime.now() - timedelta(days=int(value))
                    condition_clauses.append("date_received < %s")
                    values.append(target_date)
                elif predicate == 'less_than_months':
                    target_date = datetime.now() - timedelta(days=int(value) * 30)
                    condition_clauses.append("date_received > %s")
                    values.append(target_date)
                elif predicate == 'greater_than_months':
                    target_date = datetime.now() - timedelta(days=int(value) * 30)
                    condition_clauses.append("date_received < %s")
                    values.append(target_date)
        
        if rule_predicate == 'All':
            query += " AND ".join(condition_clauses)
        elif rule_predicate == 'Any':
            query += " OR ".join(condition_clauses)
        
        cursor.execute(query, tuple(values))
        emails = cursor.fetchall()
        
        for email in emails:
            # Perform actions
            for action in actions:
                if action == 'mark_as_read':
                    logging.info(f"Marking email {email['id']} as read.")
                    mark_as_read(email['id'])
                elif action == 'mark_as_unread':
                    logging.info(f"Marking email {email['message_id']} as unread.")
                    mark_as_unread(email['message_id'])
                elif action.startswith('move_to_folder'):
                    folder = action.split(':')[1]
                    logging.info(f"Moving email {email['id']} to folder {folder}.")
                    move_to_folder(email['id'], folder)

def mark_as_read(message_id):
    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()

def mark_as_unread(message_id):
    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'addLabelIds': ['UNREAD']}
    ).execute()

def move_to_folder(message_id, folder_name):
    label_id = get_label_id(folder_name)
    if label_id:
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'addLabelIds': [label_id], 'removeLabelIds': ['INBOX']}
        ).execute()
    else:
        logging.info(f"Label {folder_name} not found.")

def get_label_id(label_name):
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    for label in labels:
        if label['name'].lower() == label_name.lower():
            return label['id']
    return None

if __name__ == '__main__':
    apply_rules()

cursor.close()
db.close()
