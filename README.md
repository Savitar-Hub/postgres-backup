# Backup Postgres Database

This simple Python package allows you to create easily the database backup of Postgres databases.
You can upload them to cloud storage buckets by creating a cron job.

```python
    from postgres_backup import Backup

    # Instantiate the backup object with Postgres database_uri: db:engine:[//[user[:password]@][host][:port]/][dbname]
    backup = Backup(database_uri)

    # Create the file for backup
    backup.create(out_file='backup.gz')
```