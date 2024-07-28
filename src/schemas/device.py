from pydantic import BaseModel, field_validator, Field
from ..utils import PasswordValidator
from .user import UserScheme
from .location import LocationScheme


class DeviceScheme(BaseModel):
    
    login: str
    password: str 
    name: str
    device_type: str = Field(alias="type")

    location_id: int
    api_user_id: int


    @field_validator('password')
    def password_validation(cls, v: str) -> str:
        print(v)
        if PasswordValidator.validate_password(v):
            return v 
        raise ValueError("bad password")
