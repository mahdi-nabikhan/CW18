import psycopg2

db_config = {
    'dbname': 'terminal_cw18',
    'user': 'postgres',
    'password': '12345678',
    'host': 'localhost',
    'port': '4060'
}


class DatabaseManager:
    def __init__(self, db_config: dict):
        self.db_config = db_config
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = psycopg2.connect(**self.db_config)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            print(exc_val)
            self.connection.rollback()
        else:
            self.connection.commit()
        self.cursor.close()
        self.connection.close()


