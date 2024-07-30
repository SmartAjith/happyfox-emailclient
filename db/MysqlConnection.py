import mysql.connector
from mysql.connector import Error
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_connection(host_name, user_name, user_password, db_name=None):
    """ Create a database connection to the MySQL server """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        if db_name:
            logging.info(f"Connected to MySQL database '{db_name}'")
        else:
            logging.info("Connected to MySQL server")
    except Error as e:
        logging.error(f"Error: '{e}'")

    return connection
