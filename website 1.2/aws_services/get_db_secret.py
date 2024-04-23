#Retrieving database secret from AWS Secret manager
import boto3
import json
from botocore.exceptions import ClientError

# Function to retrieve the secret
def get_secret():
    # Specified the name of the secret in AWS Secrets Manager
    secret_name = "x22217029-postgres-devsecops"
    
    # Specified the AWS region where the secret is stored
    region_name = "eu-west-1"

    # Created a Secrets Manager client using the specified region
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        # Attempt to retrieve the secret value using the specified secret name
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # Handling exceptions if any occur during the retrieval
        raise e

    # Decrypting the secret using the associated KMS key and retrieve the SecretString
    secret = get_secret_value_response['SecretString']
    secret_dict = json.loads(secret)
    return secret_dict