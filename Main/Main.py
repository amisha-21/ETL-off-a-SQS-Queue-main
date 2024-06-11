from SQS_Operation import read_messages_from_queue
from DatabaseOperations import create_table

if __name__ == '__main__':
    # Set up the user_logins table first
    create_table()

    # Fetch and process messages from the SQS queue
    read_messages_from_queue()
