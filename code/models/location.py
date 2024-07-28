from peewee import CharField
from ..database import pg_db


from .base import Base


class LocationModel(Base):

    name = CharField(unique=True)

    class Meta:
        table_name = "location"
        database = pg_db