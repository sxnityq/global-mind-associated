from peewee import CharField, ForeignKeyField
from ..database import pg_db

from .base import Base
from .location import LocationModel
from .user import UserModel


class DeviceModel(Base):

    name: str = CharField()
    device_type = CharField(column_name="type")
    password = CharField()
    login = CharField(unique=True)
    location_id = ForeignKeyField(LocationModel, backref="devices",
                                   on_delete="CASCADE", field="id")
    api_user_id = ForeignKeyField(UserModel, backref="devices", on_delete="CASCADE", field="id")
    
    class Meta:
        table_name = "device"
        database = pg_db
