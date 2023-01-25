import typing


class AWSStorage:
    def __init__(
        self,
        client,
        bucket_name: typing.Optional[str] = 'backup'
    ):

        self.client = client
        self.bucket_name = bucket_name

    def list_bucket_name(self) -> typing.List[str]:
        """
        List the bucket names that we have.
        :return: list with all the names of the actual buckets
        """

        return [bucket.name for bucket in self.client.buckets.all()]
