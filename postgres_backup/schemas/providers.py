from enum import Enum


class CloudProviders(str, Enum):
    aws = 'amazon_web_services'
    gcs = 'google_cloud_storage'
