import boto3
import json

def create_secret():
    
    secret_name = 'x22217029-content-manager-postgres-secret'

    # Create an AWS Secrets Manager client
    secrets_manager = boto3.client('secretsmanager')

    # Specify the secret values (key-value pairs)
    secret_values = {
        'username': 'x22217029',
        'your_password_key': 'Admin123',
        'dbname': 'Content_Manager_Scalable'
    }

    # Create the secret in AWS Secrets Manager
    secret_response = secrets_manager.create_secret(
        Name=secret_name,
        Description='Your secret description',
        SecretString=json.dumps(secret_values)
    )

    print(f"Secret created: {secret_response['ARN']}")

    return secret_values['your_password_key']

if __name__ == "__main__":
    created_password = create_secret()
    print(f"Password created: {created_password}")