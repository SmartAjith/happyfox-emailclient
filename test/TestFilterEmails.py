import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from core.EmailProcessor import filter_emails

class TestFilterEmails(unittest.TestCase):

    @patch('core.EmailProcessor.cursor')
    def test_from_contains(self, mock_cursor):
        rule = {
            "conditions": [{"field": "From", "predicate": "contains", "value": "example.com"}],
            "predicate": "All"
        }
        mock_cursor.fetchall.return_value = [{'id': 1, 'sender': 'test@example.com', 'subject': 'Test', 'date_received': datetime.now()}]
        result = filter_emails(rule)
        self.assertEqual(len(result), 1)
        self.assertIn('test@example.com', result[0]['sender'])

    @patch('core.EmailProcessor.cursor')
    def test_from_equals(self, mock_cursor):
        rule = {
            "conditions": [{"field": "From", "predicate": "equals", "value": "test@example.com"}],
            "predicate": "All"
        }
        mock_cursor.fetchall.return_value = [{'id': 2, 'sender': 'test@example.com', 'subject': 'Exact Match', 'date_received': datetime.now()}]
        result = filter_emails(rule)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['sender'], 'test@example.com')

    @patch('core.EmailProcessor.cursor')
    def test_subject_contains(self, mock_cursor):
        rule = {
            "conditions": [{"field": "Subject", "predicate": "contains", "value": "Meeting"}],
            "predicate": "All"
        }
        mock_cursor.fetchall.return_value = [{'id': 3, 'sender': 'sender@example.com', 'subject': 'Meeting Reminder', 'date_received': datetime.now()}]
        result = filter_emails(rule)
        self.assertEqual(len(result), 1)
        self.assertIn('Meeting', result[0]['subject'])

    @patch('core.EmailProcessor.cursor')
    def test_subject_equals(self, mock_cursor):
        rule = {
            "conditions": [{"field": "Subject", "predicate": "equals", "value": "Project Update"}],
            "predicate": "All"
        }
        mock_cursor.fetchall.return_value = [{'id': 4, 'sender': 'sender@example.com', 'subject': 'Project Update', 'date_received': datetime.now()}]
        result = filter_emails(rule)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['subject'], 'Project Update')

    @patch('core.EmailProcessor.cursor')
    def test_date_received_less_than_days(self, mock_cursor):
        rule = {
            "conditions": [{"field": "Date Received", "predicate": "less_than_days", "value": "7"}],
            "predicate": "All"
        }
        recent_date = datetime.now() - timedelta(days=3)
        mock_cursor.fetchall.return_value = [{'id': 5, 'sender': 'sender@example.com', 'subject': 'Recent Email', 'date_received': recent_date}]
        result = filter_emails(rule)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['date_received'], recent_date)

    @patch('core.EmailProcessor.cursor')
    def test_date_received_greater_than_days(self, mock_cursor):
        rule = {
            "conditions": [{"field": "Date Received", "predicate": "greater_than_days", "value": "30"}],
            "predicate": "All"
        }
        older_date = datetime.now() - timedelta(days=60)
        mock_cursor.fetchall.return_value = [{'id': 6, 'sender': 'sender@example.com', 'subject': 'Old Email', 'date_received': older_date}]
        result = filter_emails(rule)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['date_received'], older_date)

    @patch('core.EmailProcessor.cursor')
    def test_date_received_less_than_months(self, mock_cursor):
        rule = {
            "conditions": [{"field": "Date Received", "predicate": "less_than_months", "value": "3"}],
            "predicate": "All"
        }
        recent_date = datetime.now() - timedelta(days=60)
        mock_cursor.fetchall.return_value = [{'id': 7, 'sender': 'sender@example.com', 'subject': 'Recent Email', 'date_received': recent_date}]
        result = filter_emails(rule)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['date_received'], recent_date)

    @patch('core.EmailProcessor.cursor')
    def test_date_received_greater_than_months(self, mock_cursor):
        rule = {
            "conditions": [{"field": "Date Received", "predicate": "greater_than_months", "value": "6"}],
            "predicate": "All"
        }
        older_date = datetime.now() - timedelta(days=200)
        mock_cursor.fetchall.return_value = [{'id': 8, 'sender': 'sender@example.com', 'subject': 'Old Email', 'date_received': older_date}]
        result = filter_emails(rule)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['date_received'], older_date)

    @patch('core.EmailProcessor.cursor')
    def test_multiple_conditions_all(self, mock_cursor):
        rule = {
            "conditions": [
                {"field": "From", "predicate": "contains", "value": "example.com"},
                {"field": "Subject", "predicate": "contains", "value": "Update"}
            ],
            "predicate": "All"
        }
        mock_cursor.fetchall.return_value = [{'id': 9, 'sender': 'sender@example.com', 'subject': 'Project Update', 'date_received': datetime.now()}]
        result = filter_emails(rule)
        self.assertEqual(len(result), 1)
        self.assertIn('example.com', result[0]['sender'])
        self.assertIn('Update', result[0]['subject'])

    @patch('core.EmailProcessor.cursor')
    def test_multiple_conditions_any(self, mock_cursor):
        rule = {
            "conditions": [
                {"field": "From", "predicate": "contains", "value": "example.com"},
                {"field": "Subject", "predicate": "contains", "value": "Meeting"}
            ],
            "predicate": "Any"
        }
        mock_cursor.fetchall.return_value = [
            {'id': 10, 'sender': 'sender@example.com', 'subject': 'Project Update', 'date_received': datetime.now()},
            {'id': 11, 'sender': 'another@example.com', 'subject': 'Meeting Reminder', 'date_received': datetime.now()}
        ]
        result = filter_emails(rule)
        self.assertEqual(len(result), 2)
        self.assertTrue(any('example.com' in email['sender'] for email in result))
        self.assertTrue(any('Meeting' in email['subject'] for email in result))

    @patch('core.EmailProcessor.cursor')
    def test_no_matching_emails(self, mock_cursor):
        rule = {
            "conditions": [{"field": "From", "predicate": "equals", "value": "nonexistent@example.com"}],
            "predicate": "All"
        }
        mock_cursor.fetchall.return_value = []
        result = filter_emails(rule)
        self.assertEqual(len(result), 0)

    @patch('core.EmailProcessor.cursor')
    def test_combination_date_and_other_fields(self, mock_cursor):
        rule = {
            "conditions": [
                {"field": "From", "predicate": "contains", "value": "example.com"},
                {"field": "Date Received", "predicate": "less_than_days", "value": "30"}
            ],
            "predicate": "All"
        }
        recent_date = datetime.now() - timedelta(days=10)
        mock_cursor.fetchall.return_value = [{'id': 12, 'sender': 'sender@example.com', 'subject': 'Email', 'date_received': recent_date}]
        result = filter_emails(rule)
        self.assertEqual(len(result), 1)
        self.assertIn('example.com', result[0]['sender'])
        self.assertTrue(result[0]['date_received'] > datetime.now() - timedelta(days=30))

if __name__ == '__main__':
    unittest.main()
