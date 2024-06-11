import boto3
import configparser
import logging

logging.basicConfig(level=logging.DEBUG)
boto3.set_stream_logger('')

def test_sqs():
    config = configparser.ConfigParser()
    config.read('/Users/amishagangwar/Downloads/ETL-off-a-SQS-Queue-main/cred.ini')
    
    aws_access_key_id = config.get('aws', 'key_id')
    aws_secret_access_key = config.get('aws', 'secret_key')
    aws_region = config.get('aws', 'region')

    # Use the correct queue URL as returned by Localstack
    queue_url = 'http://sqs.us-east-2.localhost.localstack.cloud:4566/000000000000/login-queue'

    sqs = boto3.client(
        'sqs',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
        endpoint_url='http://localhost:4566'  # Ensure this points to Localstack
    )

    try:
        # Send a test message
        send_response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody='{"user_id": "test", "device_type": "test-device"}'
        )
        print("Send Response:", send_response)

        # Receive a test message
        receive_response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )
        print("Receive Response:", receive_response)
    except boto3.exceptions.Boto3Error as e:
        print(f"Boto3 error in SQS operations: {e}")
    except Exception as e:
        print(f"General error in SQS operations: {e}")

if __name__ == "__main__":
    test_sqs()
