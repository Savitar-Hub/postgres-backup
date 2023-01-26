import gzip
import os
import typing
from datetime import date
from pathlib import Path
from subprocess import PIPE, Popen

import boto3
from google.cloud import storage
from google.oauth2 import service_account

from postgres_backup.schemas import CloudProviders, CloudStorageType
from postgres_backup.upload import AWSStorage, GCStorage
from postgres_backup.utils import logger, settings


class Backup:
    def __init__(
        self,
        db_uri: str = settings.DATABASE_URL
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
        out_file_extension: typing.Union[str, Path] = '.gz',
        table_names: typing.Optional[typing.List[str]] = [],
    ) -> str:

        username, password, host, port, db_name = self.get_db_params()

        # Set env variable needed
        os.environ['PGPASSWORD'] = password

        logger.info('Staging creation of backup')

        file_name = out_file_name \
            + '_' \
            + str(date.today()) \
            + out_file_extension

        out_path = local_file_path \
            + '/' \
            + file_name

        self.file_name = file_name
        self.local_file_path = local_file_path

        table_names = ' '.join(f'-t {table_name}' for table_name in table_names)
        command = f'pg_dump -h {host} -U {username} -d {db_name} -p 5432 {table_names} -E UTF-8'

        with gzip.open(out_path, 'wb') as f:
            p = Popen(
                command,
                stdout=PIPE,
                universal_newlines=True,
                shell=True
            )

            for stdout_line in iter(p.stdout.readline, ''):
                f.write(stdout_line.encode('utf-8'))

            p.stdout.close()
            p.wait()

        logger.info('Finished creation of backup')

        return out_path

    def upload(
        self,
        clean: typing.Optional[bool] = True,
        file_name: typing.Optional[str] = '',
        bucket_name: typing.Optional[str] = settings.BUCKET_NAME,
        remote_file_path: typing.Optional[str] = '',
        provider: typing.Optional[str] = CloudProviders.gcs.value,
        # For uploading in Google Cloud
        project_name: typing.Optional[str] = settings.PROJECT_NAME,
        google_cloud_certification: typing.Optional[
            typing.Dict[str, str]
        ] = settings.GOOGLE_CLOUD_CERTIFICATION,
        create_bucket: typing.Optional[bool] = False,
        storage_class=CloudStorageType.NEARLINE.value,
        # For uploading to AWS
        aws_server_public_key: typing.Optional[str] = settings.AWS_SERVER_PUBLIC_KEY,
        aws_server_private_key: typing.Optional[str] = settings.AWS_SERVER_PRIVATE_KEY,
        region_name: typing.Optional[str] = settings.REGION_NAME
    ):

        file_name = self.file_name if self.file_name else file_name

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
                file_name=file_name,
                local_file_path=self.local_file_path,
                remote_file_path=remote_file_path,
                clean=clean,
                create_bucket=create_bucket,
                storage_class=storage_class
            )

        elif provider == 'amazon_web_services':
            # Create a Boto3 Session
            session = boto3.Session(
                aws_server_public_key=aws_server_public_key,
                aws_server_private_key=aws_server_private_key,
                region_name=region_name
            )

            # Select the resource for which we want to work
            s3_resource = session.resource('s3')

            aws_storage = AWSStorage(
                s3_resource,
                bucket_name,
                region_name
            )

            aws_storage.upload_file(
                file_name=file_name,
                local_file_path=self.local_file_path,
                remote_file_path=remote_file_path,
                clean=clean,
                create_bucket=create_bucket,
                storage_class=storage_class
            )


if __name__ == '__main__':
    backup = Backup()

    backup.create()
