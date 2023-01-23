# Backup Postgres Database


[![Downloads](https://static.pepy.tech/personalized-badge/postgres-backup?period=month&units=none&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/postgres-backup) ![Version](https://img.shields.io/badge/version-0.1.1-blue) ![Python-Version](https://img.shields.io/badge/python-3.9-blue) ![issues](https://img.shields.io/github/issues/Nil-Andreu/postgres-backup) ![PyPI - Status](https://img.shields.io/pypi/status/postgres-backup) ![License](https://img.shields.io/github/license/Nil-Andreu/postgres-backup)

This simple Python package allows you to create easily the database backup of Postgres databases.
You can upload them to cloud storage buckets by creating a cron job.

```python
    from postgres_backup import Backup

    # Instantiate the backup object with Postgres database_uri
    backup = Backup(database_uri)

    # Create the file for backup
    backup.create(out_file='backup.gz')
```

Note that the URI has the following structure: `db:engine:[//[user[:password]@][host][:port]/][dbname]`