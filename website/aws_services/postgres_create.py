import boto3
import json

def create_rds_instance(secretPassword):
    db_instance_identifier = 'x22217029-postgres-db-scalable'
    db_instance_class = 'db.t3.micro'
    db_name = 'ContentManager'
    master_username = 'x22217029'
    secret_name = 'x22217029-content-manager-postgres-secret'
    allocated_storage = 20
    security_group_ids = ['sg-06f9cd2cc5bcaa9bd']


    rds = boto3.client('rds')

    # Retrieving the master password from AWS Secrets Manager
    secretsManager = boto3.client('secretsmanager')

    try:
        secret_response = secretsManager.get_secret_value(SecretId=secret_name)
        secret_data = json.loads(secret_response['SecretString'])
        master_password = secret_data['your_password_key']
    except secretsManager.exceptions.ResourceNotFoundException:
        # Handle the case where the secret is not found
        master_password = secretPassword

    # Creating the RDS instance
    response = rds.create_db_instance(
        DBInstanceIdentifier=db_instance_identifier,
        AllocatedStorage=allocated_storage,
        DBInstanceClass=db_instance_class,
        Engine='postgres',  
        MasterUsername=master_username,
        MasterUserPassword=master_password,
        DBName=db_name,
        VpcSecurityGroupIds=security_group_ids,
        MultiAZ=False,
        PubliclyAccessible=True,
    )

    # Waiting for the RDS instance to be available
    waiter = rds.get_waiter('db_instance_available')
    waiter.wait(DBInstanceIdentifier=db_instance_identifier)

    return master_password

if __name__ == "__main__":
    created_password = create_rds_instance(secretPassword=None)
    print(f"Password used by RDS Instance is : {created_password}")