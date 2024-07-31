import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from MysqlConnection import create_connection
from mysql.connector import Error
import logging
from util.DBConfig import read_db_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_table(connection):
    """ Create the emails table with auto-incrementing id """
    if connection is not None:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS emails (
            id VARCHAR(255) PRIMARY KEY,
            sender VARCHAR(255),
            recipient TEXT,
            subject VARCHAR(255),
            date_received DATETIME,
            snippet TEXT,
            INDEX idx_date_received (date_received),
            INDEX idx_subject (subject),
            INDEX idx_sender (sender),
            INDEX idx_snippet (snippet(255))
        );
        """
        cursor = connection.cursor()
        try:
            cursor.execute(create_table_query)
            connection.commit()
            logging.info("Table 'emails' created successfully")
        except Error as e:
            logging.error(f"Error: '{e}'")
        finally:
            cursor.close()
    else:
        logging.error("Error! Cannot create the table connection.")

def main():
    db_config = read_db_config()
    connection = create_connection(db_config['host'], db_config['user'], db_config['password'], db_config['database'])
    create_table(connection)
    if connection is not None and connection.is_connected():
        connection.close()

if __name__ == "__main__":
    main()