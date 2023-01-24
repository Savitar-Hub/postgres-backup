import gzip
import os
import typing
from datetime import date
from pathlib import Path

from google.cloud import storage
from google.oauth2 import service_account
from logger import logger

from postgres_backup.schemas import CloudProviders, CloudStorageType
from postgres_backup.upload import GCStorage

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
        self.file_name = None
        self.local_file_path = None  # Store local file system location of backup file stored

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
        local_file_path: typing.Optional[str] = '',
        out_file_name: typing.Union[str, Path] = 'backup',
        out_file_extension: typing.Union[str, Path] = '.gz'
    ) -> str:

        username, password, host, port, db_name = self.get_db_params()

        # Set env variable needed
        os.environ['PGPASSWORD'] = password

        logger.info('Staging creation of backup')

        file_name = out_file_name \
            + '/' \
            + str(date.today()) \
            + out_file_extension

        out_path = local_file_path \
            + '/' \
            + file_name

        self.file_name = file_name
        self.local_file_path = local_file_path

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
        clean: typing.Optional[bool] = True,
        bucket_name: typing.Optional[str] = 'backup',
        remote_file_path: typing.Optional[str] = '',
        provider: typing.Optional[str] = CloudProviders.gcs.value,
        # For uploading in Google Cloud
        project_name: typing.Optional[str] = '',
        google_cloud_certification: typing.Optional[
            typing.Dict[str, str]
        ] = None,
        create_bucket: typing.Optional[bool] = False,
        storage_class=CloudStorageType.NEARLINE.value
    ):

        if provider == 'google_cloud_storage':
            credentials = service_account.Credentials.from_service_account_info(
                google_cloud_certification
            )

            client = storage.Client(
                project=project_name,
                credentials=credentials
            )
            gcs_storage = GCStorage(client=client, bucket_name=bucket_name)
            gcs_storage.upload_file(
                file_name=self.file_name,
                local_file_path=self.local_file_path,
                remote_file_path=remote_file_path,
                clean=clean,
                create_bucket=create_bucket,
                storage_class=storage_class
            )
