import boto3
import psycopg2
import configparser
import json
from cryptography.fernet import Fernet
from botocore.exceptions import ClientError, BotoCoreError

def get_sqs_messages(sqs, queue_url):
    try:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10,
            MessageAttributeNames=['All'],
            AttributeNames=['All']
        )
        print(f"Received response: {response}")
        messages = response.get('Messages', [])
        return messages
    except ClientError as e:
        print(f"Client error receiving messages: {e}")
        return []
    except BotoCoreError as e:
        print(f"BotoCore error receiving messages: {e}")
        return []
    except Exception as e:
        print(f"General error receiving messages: {e}")
        return []

def mask_data(value, cipher_suite):
    return cipher_suite.encrypt(value.encode()).decode()

def transform_message(message, cipher_suite):
    body = json.loads(message['Body'])

    return {
        'user_id': body.get('user_id', 'unknown'),
        'device_type': body.get('device_type', 'unknown'),
        'masked_ip': mask_data(body.get('ip', '0.0.0.0'), cipher_suite),
        'masked_device_id': mask_data(body.get('device_id', 'unknown'), cipher_suite),
        'locale': body.get('locale', 'unknown'),
        'app_version': int(body.get('app_version', '0')),
        'create_date': body.get('create_date', '1970-01-01')
    }

def write_to_postgres(data, conn):
    with conn.cursor() as cursor:
        insert_query = """
        INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)
        VALUES (%(user_id)s, %(device_type)s, %(masked_ip)s, %(masked_device_id)s, %(locale)s, %(app_version)s, %(create_date)s)
        """
        cursor.execute(insert_query, data)
    conn.commit()

def main():
    config = configparser.ConfigParser()
    config.read('/Users/amishagangwar/Downloads/ETL-off-a-SQS-Queue-main/cred.ini')
    
    aws_access_key_id = config.get('aws', 'key_id')
    aws_secret_access_key = config.get('aws', 'secret_key')
    aws_region = config.get('aws', 'region')

    postgres_config = {
        'dbname': config.get('postgres', 'dbname'),
        'user': config.get('postgres', 'user'),
        'password': config.get('postgres', 'password'),
        'host': config.get('postgres', 'host'),
        'port': config.get('postgres', 'port')
    }

    queue_url = 'http://sqs.us-east-2.localhost.localstack.cloud:4566/000000000000/login-queue'

    # Replace with your actual encryption key
    encryption_key = b"Os6ERuqAbLS-oOfP1eyjKcNSSlgKvs7NdqORSZQPKJg="  # Replace this with the key you generated

    # Validate the key length
    if len(encryption_key) != 44:
        print("Invalid encryption key length. It must be 44 bytes.")
        return

    cipher_suite = Fernet(encryption_key)

    sqs = boto3.client(
        'sqs',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
        endpoint_url='http://localhost:4566'
    )

    try:
        conn = psycopg2.connect(**postgres_config)
    except Exception as e:
        print(f"Error connecting to Postgres: {e}")
        return

    # Get queue attributes to check visibility timeout
    try:
        queue_attributes = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['All'])
        print(f"Queue attributes: {queue_attributes}")
    except Exception as e:
        print(f"Error getting queue attributes: {e}")

    messages = get_sqs_messages(sqs, queue_url)
    print(f"Received {len(messages)} messages")

    for message in messages:
        try:
            transformed_data = transform_message(message, cipher_suite)
            print(f"Transformed data: {transformed_data}")  # Verify transformed data
            write_to_postgres(transformed_data, conn)
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
            print(f"Message processed and deleted: {message['MessageId']}")
        except KeyError as e:
            print(f"Missing key in message: {e}")
        except ClientError as e:
            print(f"Client error deleting message: {e}")
        except Exception as e:
            print(f"Error processing message: {e}")

    conn.close()

if __name__ == "__main__":
    main()
