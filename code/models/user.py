from peewee import CharField
from ..database import pg_db


from .base import Base


class UserModel(Base):

    name        = CharField(unique=True)
    email       = CharField(unique=True)
    password    = CharField()

    class Meta:
        table_name  = "api_user"
        database    = pg_db 