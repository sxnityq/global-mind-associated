from aiohttp import BasicAuth
from aiohttp.web import Request, HTTPBadRequest, HTTPCreated, Response
from pydantic import  ValidationError
from json import JSONDecoder, JSONEncoder
from hashlib import sha256

from ..schemas.device import DeviceScheme
from ..models.device import DeviceModel
from ..models.user import UserModel
from ..models.location import LocationModel
from ..utils.model_serializer import basic_serializer
from ..utils.password_validator import PasswordValidator


class DeviceHandler:

    decoder =  JSONDecoder()
    encoder =  JSONEncoder()


    def __init__(self) -> None:
        pass

    async def get_device(self, request: Request):
        
        device_id       = request.match_info.get("device_id")
        model           = DeviceModel.get_or_none(DeviceModel.id == device_id)
        
        if model is None:
            return HTTPBadRequest(reason=f"Device with id {device_id} does not exist")
        
        user_model      =   UserModel.get_by_id(model.api_user_id)
        location_model  = LocationModel.get_by_id(model.location_id)
        
        ser_location    = basic_serializer(location_model)
        ser_user        = basic_serializer(user_model)
        
        ser_user.pop("password")
        
        return Response(body=self.encoder.encode({
            "id": model.id, 
            "name": model.name,
            "device_type": model.device_type,
            "login": model.login,
            "location_id": ser_location,
            "api_user_id": ser_user}))

    async def create_device(self, request: Request):
        
        if not request.has_body:
            return HTTPBadRequest(text="no request body provided. Aborted")
        
        body            = await request.text()
        body            = self.decoder.decode(body)
        auth            = BasicAuth.decode(request.headers.get("Authorization"),
                                            encoding="utf-8")
        user            = UserModel.get(UserModel.name == auth.login)
        
        try:
            DeviceScheme(**body, api_user_id=user.id)
        except ValidationError as e:
            return HTTPBadRequest(text=e.json())
        
        location_id     = body.get("location_id")
        device_login    = body.get("login")
        device_type     = body.get("type")
        device_name     = body.get("name")
        device_password = sha256(body.get("password").encode('utf-8')).hexdigest()

        location = LocationModel.get_or_none(LocationModel.id == location_id)
        
        if location is None:
            return HTTPBadRequest(reason=f"location with id {location_id} does not exist")
        
        if DeviceModel.get_or_none(DeviceModel.login == device_login) is not None:
            return HTTPBadRequest(reason=f"location with login {device_login} already exist")

        DeviceModel.create(name=device_name, 
                           login=device_login,
                           password=device_password,
                           device_type=device_type,
                           location_id=location_id,
                           api_user_id=user.id)
        
        return HTTPCreated(text=f"device with name {device_name} created")
    

    async def update_device(self, request: Request):
        
        device_id       = request.match_info.get("device_id")
        model           = DeviceModel.get_or_none(DeviceModel.id == device_id)
        
        if model is None:
            return HTTPBadRequest(reason=f"Device with id {device_id} does not exist")
        
        body            = await request.text()
        body            = self.decoder.decode(body)

        device_name     = body.get("name", model.name)
        device_login    = body.get("login", model.login)
        device_type     = body.get("type", model.device_type)

        location_id     = body.get("location_id", model.location_id)
        api_user_id     = body.get("api_user_id", model.api_user_id)

        if LocationModel.get_by_id(location_id) is None:
            return HTTPBadRequest(f"location with id {location_id} does not exist")
        
        if UserModel.get_by_id(api_user_id) is None:
            return HTTPBadRequest(f"user with id {api_user_id} does not exist")
        
        device_password = body.get("password")
        
        if device_password is not None:
            if PasswordValidator.validate_password(device_password):
                device_password = sha256(device_password.encode('utf-8')).hexdigest()
        else:
            device_password = model.password
        
        DeviceModel.update({
            DeviceModel.name: device_name,
            DeviceModel.login: device_login,
            DeviceModel.password: device_password,
            DeviceModel.device_type: device_type,
            DeviceModel.location_id: location_id,
            DeviceModel.api_user_id: api_user_id}).execute()
        
        return Response(reason="device successfully updated")

    async def delete_device(self, request: Request):
        
        device_id   = request.match_info.get("device_id")
        model       = DeviceModel.get_or_none(DeviceModel.id == device_id)
        
        if model is None:
            return HTTPBadRequest(reason=f"Device with id {device_id} does not exist")
        
        DeviceModel.delete_by_id(device_id)
        return Response(reason=f"device with id {device_id} successfully deleted")