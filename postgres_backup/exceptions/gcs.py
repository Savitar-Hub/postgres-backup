
class BucketError(Exception):
    def __init__(
        self,
        msg: str = 'Error with the bucket'
    ):

        self.msg = msg
        super().__init__(self.msg)
