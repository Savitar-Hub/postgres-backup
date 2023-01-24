import datetime as dt
import os
import typing

from google.cloud import storage
from google.cloud.storage.bucket import Bucket
from google.cloud.storage.client import Client
from google.oauth2 import service_account

from postgres_backup.exceptions.gcs import BucketError
from postgres_backup.schemas.gcs import CloudStorageType


class GCStorage:
    def __init__(
            self,
            client,
            bucket_name: typing.Optional[str] = 'backup'
    ):

        self.client = client
        self.bucket_name = bucket_name

    @staticmethod
    def _validate_bucket(self) -> bool:
        """
        Validation of the bucket that we provided.

        :param self:
        :return: True if it is a valid bucket
        """

        bucket_list = self.list_bucket_name()

        if self.bucket_name not in bucket_list:
            raise BucketError(
                msg=f'Bucket {self.bucket_name} not found'
            )

        return True

    @staticmethod
    def _validate_new_bucket(self, storage_class: str):
        """
        Validate if the new bucket we want to crreate is of a valid storage class
        :param self:
        :param storage_class: the type of bucket we want to create
        :return: True if created correctly
        """

        valid_storage_class = [storage_class.value for storage_class in CloudStorageType]
        if storage_class not in valid_storage_class:
            raise BucketError(
                msg=f'Bucket storage class: {storage_class} invalid\nShould be in: {valid_storage_class}'
            )

        if self._validate_bucket(self):
            raise BucketError(
                msg=f'Bucket {self.bucket_name} already exists'
            )

    @staticmethod
    def _get_bucket(self):
        """
        Get the bucket object from google

        :param self:
        :return: bucket instance
        """

        self._validate_bucket(self)

        return self.client.get_bucket(self.bucket_name)

    def list_bucket_name(self) -> typing.List[str]:
        """
        List the bucket names that we have.

        :return: list with all the names of the actual buckets
        """

        return [bucket.name for bucket in self.client.list_buckets()]

    def create_bucket(
        self,
        storage_class: str = CloudStorageType.STANDARD.value
    ):
        """
        In the case we do not have a bucket already created for storing backups, we can create it.
        :param storage_class: the type of bucket we want to create
        :return: True if created correctly storage class
        """

        self._validate_new_bucket(self, storage_class)
        self.client.create_bucket(self.bucket_name, storage_class)

        return True