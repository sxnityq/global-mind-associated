from aiohttp.web import Request, HTTPBadRequest, HTTPCreated, Response
from pydantic import  ValidationError
from json import JSONDecoder, JSONEncoder
from peewee import ModelObjectCursorWrapper


from ..schemas import LocationScheme
from ..models import LocationModel

class LocationHandler:

    decoder =  JSONDecoder()
    encoder =  JSONEncoder()

    def __init__(self) -> None:
        pass

    """GET"""
    async def get_location(self, request: Request):
        location_id = request.match_info.get("location_id", "")
        model = LocationModel.get_or_none(LocationModel.id == location_id)
        if model is None:
            return HTTPBadRequest(reason=f"Location with id {location_id} does not exist")
        return Response(body=self.encoder.encode({"id": model.id, "name": model.name}))

    """POST"""
    async def create_location(self, request: Request):
        if not request.has_body:
            return HTTPBadRequest(reason="no request body provided. Aborted")
        body = await request.text()
        body = self.decoder.decode(body)
        location_name = body.get("name")
        try:
            LocationScheme(**body)  
            LocationModel.create(name=location_name)
        except ValidationError as e:
            return HTTPBadRequest(text=e.json())
        except Exception as e:
            return HTTPBadRequest(reason=f"location {location_name} already exist")
        return HTTPCreated(reason=f"location {location_name} successfully created")
    
    """PUT"""
    async def update_location(self, request: Request):
        location_id = request.match_info.get("location_id")
        if not request.has_body:
            return HTTPBadRequest(reason="no request body provided. Aborted")
        body = await request.text()
        body = self.decoder.decode(body)
        try:
            scheme = LocationScheme(**body)
            q = LocationModel.update({LocationModel.name: scheme.name}).where(LocationModel.id == location_id)
            if q.execute() == 0:
                return Response(body=f"Location with id {location_id} does not exist")
        except Exception as e:
            return HTTPBadRequest(reason=e)
        return Response(body=f"name field successfully updated to {scheme.name} value")

    """DELETE"""    
    async def delete_location(self, request: Request):
        location_id = request.match_info.get("location_id")
        q = LocationModel.delete_by_id(location_id)
        if q == 0:
            return Response(body=f"Location with id {location_id} does not exist")
        return Response(body=f"location with id {location_id} successfully deleted")

    