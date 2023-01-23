from enum import Enum


class CloudProviders(str, Enum):
    aws: str = 'amazon_web_services'
    gcs: str = 'google_cloud_storage'
