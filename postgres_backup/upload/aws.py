import os
import typing


class AWSStorage:
    def __init__(
        self,
        s3_resource,
        region_name: typing.Optional[str],
        bucket_name: typing.Optional[str] = 'backup',
    ):

        self.s3_resource = s3_resource
        self.bucket_name = bucket_name
        self.region_name = region_name

    def list_bucket_name(self) -> typing.List[str]:
        """
        List the bucket names that we have.
        :return: list with all the names of the actual buckets
        """

        return [bucket.name for bucket in self.s3_resource.buckets.all()]

    def create_bucket(self):
        """
        In the case we do not have a bucket already created for storing backups, we can create it.
        :param storage_class: the type of bucket we want to create
        :return: True if created correctly storage class
        """

        self.s3_resource.create_bucket(
            Bucket=self.bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': self.region_name
            }
        )

        return True

    def upload_file(
        self,
        file_name,
        local_file_path,
        remote_file_path,
        clean,
        create_bucket,
    ):
        """
        :param local_file_path: where is the path of folders where we have the file
        :param remote_file_path: path if folders where we want to store the backup file in the bucket
        :param file_name: where it is the file from our local file system
        :param clean: if we want to remove the backup file from local file system
        :param create_bucket: if for that upload of file, we want to first create the bucket for backups
        :param storage_class: the type of storage bucket for storing backups
        :return: True if created correctly
        """

        if create_bucket:
            self.create_bucket()

        self.s3_resource.meta.client.upload_file(
            local_file_path + '/' + file_name,
            self.bucket_name,
            remote_file_path
        )

        if clean:
            os.remove(local_file_path + '/' + file_name)
