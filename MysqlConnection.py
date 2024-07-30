import mysql.connector
from mysql.connector import Error

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
            print(f"Connected to MySQL database '{db_name}'")
        else:
            print(f"Connected to MySQL server")
    except Error as e:
        print(f"Error: '{e}'")

    return connection
