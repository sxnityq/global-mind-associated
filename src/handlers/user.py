from aiohttp.web import Request, HTTPBadRequest, Response, HTTPCreated, HTTPForbidden
from pydantic import  ValidationError
from json import JSONDecoder, JSONEncoder
from hashlib import sha256
from aiohttp import BasicAuth
from peewee import IntegrityError

from ..schemas.user import UserScheme, UserAuth
from ..utils.password_validator import PasswordValidator
from ..utils.email_validator import EmailValidator
from ..utils.base64_auth_generator import gen_base64
from ..models.user import UserModel


class UserHandler:

    decoder =  JSONDecoder()
    encoder =  JSONEncoder()


    def __init__(self) -> None:
        pass


    async def get_user(self, request: Request):
        
        user_id         = request.match_info.get("user_id")
        model           = UserModel.get_or_none(UserModel.id == user_id)
        
        if model is None:
            return HTTPBadRequest(reason=f"User with id {user_id} does not exist")
    
        devices = []

        for device in model.devices:
            d = device.__dict__['__data__']
            d.pop("password")
            devices.append(d)

        return Response(body=self.encoder.encode({
            "name": model.name,
            "email": model.email,
            "devices": devices}))


    async def create_user(self, request: Request):
        
        if not request.has_body:
            return HTTPBadRequest(text="no request body provided. Aborted")
        
        body        = await request.text()
        body        = self.decoder.decode(body)
        
        try:
            UserScheme(**body)  
        except ValidationError as e:
            return HTTPBadRequest(text=e.json())
        
        try:
            UserModel.create(name=body.get("name"), 
                        password=sha256(body.get("password").encode('utf-8')).hexdigest(),
                        email=body.get("email"))
            base64 = gen_base64(body.get("name"), body.get("password"))
            return HTTPCreated(text=base64)
        except Exception as e:
            return HTTPBadRequest(body="user name or email already exist")
        
        
    async def update_user(self, request: Request):
        
        if not request.has_body:
            return Response(body="No body provided. Nothing to update")
        
        user_id     = request.match_info.get("user_id")
        auth        = BasicAuth.decode(request.headers.get("Authorization"),
                                        encoding="utf-8")
        model       = UserModel.get_or_none(UserModel.id == user_id)
        
        if model is None:
            return HTTPBadRequest(reason=f"user with id {user_id} does not exist")
        
        if auth.login != model.name:
            return HTTPForbidden(reason="no way bro")
        
        body        = await request.text()
        body        = self.decoder.decode(body)
        
        user_auth   = UserAuth(login=auth.login, password=auth.password)
        user_email  = body.get("email", model.email)
        user_name   = body.get("name", model.name)
        user_password = body.get("password")
        
        if model.name == user_name:
            return HTTPBadRequest(reason=f"user with name {user_name} already exist")
        if model.email == user_email:
            return HTTPBadRequest(reason=f"user with email {user_email} already exist")

        if user_password is not None:
            if not PasswordValidator.validate_password(user_password):
                return HTTPBadRequest(reason="password validation error")
            user_auth.password = user_password
            user_password = sha256(user_password.encode('utf-8')).hexdigest()
        else:
            user_password = model.password
        
        if not EmailValidator.validate_email(user_email):
            return HTTPBadRequest(reason="email validation error")
        
        user_auth.login = user_name

        UserModel.update({UserModel.name: user_name,
                          UserModel.password: user_password,
                          UserModel.email: user_email}).where(
                              UserModel.id == user_id
                          ).execute()
        
        new_base64=gen_base64(user_auth.login, user_auth.password)
        return Response(text=new_base64)
    

    async def delete_user(self, request: Request):
        
        user_id = request.match_info.get("user_id")
        auth = BasicAuth.decode(request.headers.get("Authorization"), encoding="utf-8")
        model = UserModel.get_or_none(UserModel.id == user_id)
        
        if model is None:
            return HTTPBadRequest(reason=f"user with id {user_id} does not exist")
        
        if auth.login != model.name:
            return HTTPForbidden(reason="no way bro")
        
        UserModel.delete_by_id(user_id)
        return Response(body=f"user with id {user_id} successfully deleted")
