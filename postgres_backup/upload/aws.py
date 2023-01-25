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
