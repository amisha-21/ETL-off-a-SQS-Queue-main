import psycopg2

def connect_to_database():
    #Establish and return a connection to the PostgreSQL database.
    return psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )

def create_table():
    #Ensure the 'user_logins' table exists in the database.
    try:
        # Set up a connection and cursor
        with connect_to_database() as connection, connection.cursor() as cursor:
            
            # Define the SQL command to create the user_logins table
            create_table_command = """
            CREATE TABLE IF NOT EXISTS user_logins(
                user_id varchar(128),
                device_type varchar(32),
                masked_ip varchar(256),
                masked_device_id varchar(256),
                locale varchar(32),
                app_version varchar(32),
                create_date date
            );
            """

            cursor.execute(create_table_command)
            connection.commit()
        
    except Exception as e:
        print(f"Failed to create table: {e}")

def store_data_in_postgres(data: dict):
    #Insert the given data into the user_logins table.
    try:
        # Setting up connection and cursor
        with connect_to_database() as connection, connection.cursor() as cursor:

            # Define the SQL command to insert a new record
            insert_command = """INSERT INTO user_logins (user_id, device_type, masked_ip, 
                          masked_device_id, locale, app_version, create_date) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s)"""

            # Prepare the record to be inserted
            record = (
                data.get('user_id'), 
                data.get('device_type'), 
                data.get('masked_ip'),
                data.get('masked_device_id'),
                data.get('locale'), 
                data.get('app_version'), 
                data.get('create_date', None)
            )
            
            cursor.execute(insert_command, record)
            connection.commit()
            
    except Exception as e:
        print(f"Failed to store data in database: {e}")
