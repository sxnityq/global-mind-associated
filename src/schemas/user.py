from pydantic import BaseModel, field_validator
from ..utils import PasswordValidator, EmailValidator

from dataclasses import dataclass

class UserScheme(BaseModel):
    
    password: str 
    name: str
    email: str

    @field_validator('password')
    def password_validation(cls, v: str) -> str:
        print(v)
        if PasswordValidator.validate_password(v):
            return v 
        raise ValueError("bad password")
    
    @field_validator('email')
    def email_validation(cls, v: str) -> str:
        if EmailValidator.validate_email(v):
            return v 
        raise ValueError("bad email")


@dataclass
class UserAuth:
    login: str
    password: str