import boto3
import json
import os
from botocore.exceptions import ClientError

def get_secret(secret_name, region_name='us-east-1'):
    """
    Retrieve secret from AWS Secrets Manager
    Falls back to environment variable if Secrets Manager is not available
    """
    # First try environment variable (for local development)
    env_value = os.getenv(secret_name)
    if env_value:
        return env_value
    
    # Try AWS Secrets Manager
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        
        # Parse the secret
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            # If it's JSON, parse it
            try:
                secret_dict = json.loads(secret)
                return secret_dict
            except json.JSONDecodeError:
                # It's a plain string
                return secret
        
    except ClientError as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        return None
    
    return None

def get_spotify_credentials(region_name='us-east-1'):
    """Get Spotify credentials from Secrets Manager or environment"""
    # Try environment variables first
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if client_id and client_secret:
        return {'client_id': client_id, 'client_secret': client_secret}
    
    # Try Secrets Manager
    secret = get_secret('spotify-credentials', region_name)
    if isinstance(secret, dict):
        return {
            'client_id': secret.get('client_id'),
            'client_secret': secret.get('client_secret')
        }
    return None

