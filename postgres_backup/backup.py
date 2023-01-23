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

    def get_db_params(
        self,
    ):
        user_pass, host_db = self.db_uri.split('@')

        username, password = user_pass.split(':')[1:]
        username = username.split('//')[1]

        host, port_database = host_db.split(':')
        port, db_name = port_database.split('/')

        return username, password, host, port, db_name


