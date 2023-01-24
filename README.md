# Backup Postgres Database


[![Downloads](https://static.pepy.tech/personalized-badge/postgres-backup?period=month&units=none&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/postgres-backup) ![Version](https://img.shields.io/badge/version-0.1.1-blue) ![Python-Version](https://img.shields.io/badge/python-3.9-blue) ![issues](https://img.shields.io/github/issues/Nil-Andreu/postgres-backup) ![PyPI - Status](https://img.shields.io/pypi/status/postgres-backup) ![License](https://img.shields.io/github/license/Nil-Andreu/postgres-backup)


## Basic Usage

This simple Python package allows you to create easily the database backup of Postgres databases.
You can upload them to cloud storage buckets by creating a cron job.

```python
    from postgres_backup import Backup

    # Instantiate the backup object with Postgres database_uri
    backup = Backup()

    # Create the file for backup
    backup.create()
```

You should have as environment variable `DATABASE_URL`, which is the URI of the Postgres database.
This URI has the following structure: `db:engine:[//[user[:password]@][host][:port]/][dbname]`.

## Why?

This package has proved experience of working well for databases of small-mid size.

Doing this, you make sure you can store your database backups without relying in only one cloud provider or region.

## Bucket Storage

Have provided the ability to store those backups in cloud buckets.

### Google Cloud Storage

For using this functionality, you need to install the dependencies needed of the package:
```bash
    pip3 install "postgres-backup[gcs]"
```
This basically will install also the `google` package.

And then after we have the backup created, we would keep following with:
```python
    # Upload it to google cloud storage
    backup.upload(
        provider=CloudProviders.gcs.value,
    )
```

Where the `google_cloud_certification` is a dictionary, with the key-values of the client api keys:
```python
    google_cloud_credentials = {
      "type": "service_account",
      "project_id": "xxx-saas",
      "private_key_id": "xxxxxxxx",
      "private_key": "-----BEGIN PRIVATE KEY-----\nxxxxxxxxxx\n-----END PRIVATE KEY-----\n",
      "client_email": "xxx@xxx-saas.iam.gserviceaccount.com",
      "client_id": "xxx",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/xxx%xxx-saas.iam.gserviceaccount.com"
    }
```

Recommended to provide each key as an environmental variable:
- GOOGLE_CLOUD_TYPE -> type
- GOOGLE_CLOUD_PROJECT_ID -> project_id
- GOOGLE_CLOUD_PRIVATE_KEY_ID -> private_key_id
- GOOGLE_CLOUD_PRIVATE_KEY -> private_key
- GOOGLE_CLOUD_CLIENT_EMAIL -> client_email
- GOOGLE_CLOUD_CLIENT_ID -> client_id
- GOOGLE_CLOUD_AUTH_URI -> auth_uri
- GOOGLE_CLOUD_TOKEN_URI -> token_uri
- GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL -> auth_provider_x509_cert_url
- GOOGLE_CLOUD_CLIENT_X509_CERT_URL -> client_x509_cert_url

Moreover `PROJECT_NAME` and `BUCKET_NAME` of the google bucket, and finally `DATABASE_URL` of Postgres database.


In the case that we do not have a bucket already created for storing the backups, we could add additional parameters to create it:
```python
    from postgres_backup.schemas import CloudStorageType, CloudProviders

    backup.upload(
        provider=CloudProviders.gcs.value,
        bucket_name=bucket_name,
        create_bucket=True,
        storage_class=CloudStorageType.NEARLINE.value
    )
```
