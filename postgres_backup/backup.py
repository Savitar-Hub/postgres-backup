import os

try:
    from sh import pg_dump

except ImportError as e:
    print('You must have postgresql client installed: pg_dump not found')
    os.system('apt-get install postgresql-client')


class Backup:
    def __init__(
        self,
        db_uri: str
    ):

        self.db_uri = db_uri



