import os
import gzip
import typing
from pathlib import Path
from logger import logger

from upload.providers import CloudProviders


try:
    from sh import pg_dump

except ImportError as e:
    logger.error(f'You must have sh & postgresql client installed: {e}')


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
    ) -> str:

        username, password, host, port, db_name = self.get_db_params()

        # Set env variable needed
        os.environ['PGPASSWORD'] = password

        logger.info('Staging creation of backup')

        with gzip.open(out_path, 'wb') as f:
            pg_dump(
                '-h',
                host,
                '-U',
                username,
                db_name,
                '-E UTF-8',
                _out=f)

        logger.info('Finished creation of backup')

        return out_path

    def upload(
        self,
        bucket_name: str = 'backup',
        provider: CloudProviders = CloudProviders.gcs,
    ):
        pass
