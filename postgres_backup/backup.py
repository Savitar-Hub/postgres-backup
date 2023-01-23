import os
from pathlib import Path

import typing

try:
    from sh import pg_dump

except ImportError as e:
    print('You must have postgresql client installed: pg_dump not found')
    os.system('apt-get install postgresql-client')

try:
    import gzip

except ImportError as e:
    print('You must have gzip package: gzip not found')


class Backup:
    def __init__(
        self,
        db_uri: str
    ):

        self.db_uri = db_uri

    def get_db_params(
        self,
    ) -> typing.Tuple[str, str, str, str, str]:

        user_pass, host_db = self.db_uri.split('@')

        username, password = user_pass.split(':')[1:]
        username = username.split('//')[1]

        host, port_database = host_db.split(':')
        port, db_name = port_database.split('/')

        return username, password, host, port, db_name

    def create(
        self,
        out_path: typing.Union[str, Path] = 'backup.gz'
    ):
        username, password, host, port, db_name = self.get_db_params()

        with gzip.open(out_path, 'wb') as f:
            pg_dump(
                '-h',
                host,
                '-U',
                username,
                db_name,
                '-E UTF-8',
                _out=f)


