import os
import boto3
from base64 import b64decode
from botocore.exceptions import ClientError
from collections import namedtuple
import json


Secrets = namedtuple('Secrets', 'live,sandbox')
APICredentials = namedtuple('APICredentials', 'api_key,secret,passphrase,payment_name')


def get_secrets():
    '''
    Returns sandbox and live credentials structured as:

    secrets.[live,sandbox].[passphrase,api_key,secret]
    '''
    session = boto3.session.Session()
    client = session.client('secretsmanager', region_name='us-east-1')

    return Secrets(
        live=_get_secret(client, 'prod/coinbase_pro'),
        sandbox=_get_secret(client, 'sandbox/coinbase_pro')
    )

def _get_secret(secrets_manager, secret_name):
    '''Fetch secret from AWS'''
    try:
        get_secret_value_response = secrets_manager.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            creds = json.loads(get_secret_value_response['SecretString'])
            return APICredentials(**creds)
        else:
            print('Missing SecretString in secret response')
