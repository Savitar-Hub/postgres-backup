import os
import typing

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL')

    PROJECT_NAME: str = os.getenv('PROJECT_NAME')
    BUCKET_NAME: str = os.getenv('BUCKET_NAME')

    # AWS information
    AWS_SERVER_PUBLIC_KEY: str = os.getenv('AWS_SERVER_PUBLIC_KEY')
    AWS_SERVER_PRIVATE_KEY: str = os.getenv('AWS_SERVER_PRIVATE_KEY')
    REGION_NAME: str = os.getenv('REGION_NAME')

    # Google Cloud Certification information
    GOOGLE_CLOUD_TYPE = os.getenv('GOOGLE_CLOUD_TYPE')
    GOOGLE_CLOUD_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    GOOGLE_CLOUD_PRIVATE_KEY_ID = os.getenv('GOOGLE_CLOUD_PRIVATE_KEY_ID')
    GOOGLE_CLOUD_PRIVATE_KEY = os.getenv('GOOGLE_CLOUD_PRIVATE_KEY', '').replace('\\n', '\n')
    GOOGLE_CLOUD_CLIENT_EMAIL = os.getenv('GOOGLE_CLOUD_CLIENT_EMAIL')
    GOOGLE_CLOUD_CLIENT_ID = os.getenv('GOOGLE_CLOUD_CLIENT_ID')
    GOOGLE_CLOUD_AUTH_URI = os.getenv('GOOGLE_CLOUD_AUTH_URI')
    GOOGLE_CLOUD_TOKEN_URI = os.getenv('GOOGLE_CLOUD_TOKEN_URI')
    GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL = os.getenv(
        'GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL'
    )
    GOOGLE_CLOUD_CLIENT_X509_CERT_URL = os.getenv('GOOGLE_CLOUD_CLIENT_X509_CERT_URL')

    GOOGLE_CLOUD_CERTIFICATION: typing.Dict[
        str,
        typing.Union[None, str]
    ] = {
        'type': GOOGLE_CLOUD_TYPE,
        'project_id': GOOGLE_CLOUD_PROJECT_ID,
        'private_key_id': GOOGLE_CLOUD_PRIVATE_KEY_ID,
        'private_key': GOOGLE_CLOUD_PRIVATE_KEY,
        'client_email': GOOGLE_CLOUD_CLIENT_EMAIL,
        'client_id': GOOGLE_CLOUD_CLIENT_ID,
        'auth_uri': GOOGLE_CLOUD_AUTH_URI,
        'token_uri': GOOGLE_CLOUD_TOKEN_URI,
        'auth_provider_x509_cert_url': GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL,
        'client_x509_cert_url': GOOGLE_CLOUD_CLIENT_X509_CERT_URL,
    }

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False
        env_nested_delimiter = '__'


settings = Settings()
