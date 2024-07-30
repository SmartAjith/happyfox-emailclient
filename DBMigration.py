# create_table.py
from MysqlConnection import create_connection
from mysql.connector import Error

def create_table(connection):
    """ Create the emails table """
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
            print("Table 'emails' created successfully")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            cursor.close()
    else:
        print("Error! Cannot create the table connection.")

def main():    
    connection = create_connection("localhost", "root", "root", "happyFoxEmails")
    create_table(connection)
    if connection is not None and connection.is_connected():
        connection.close()

if __name__ == "__main__":
    main()
