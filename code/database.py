from peewee import PostgresqlDatabase

from .config import DB_USER, DB_PASS, DB_NAME, DB_HOST, DB_PORT


pg_db = PostgresqlDatabase(database=DB_NAME, user=DB_USER,
                           password=DB_PASS, host=DB_HOST, port=DB_PORT)