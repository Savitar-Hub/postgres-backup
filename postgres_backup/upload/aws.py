import typing


class AWSStorage:
    def __init__(
        self,
        client,
        bucket_name: typing.Optional[str] = 'backup'
    ):

        self.client = client
        self.bucket_name = bucket_name
