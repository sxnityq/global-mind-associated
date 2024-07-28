from aiohttp import web

from code.handlers import UserHandler, DeviceHandler, LocationHandler
from code.database import pg_db

from code.models import DeviceModel, UserModel, LocationModel
from code.middlewares.auth import auth_middleware


pg_db.connect()
pg_db.create_tables([DeviceModel, UserModel, LocationModel])


middlewares=[auth_middleware]

app = web.Application(middlewares=middlewares)
user_handler = UserHandler()
device_handler = DeviceHandler()
location_handler = LocationHandler()

app.add_routes([
                web.get("/user/get/{user_id}", user_handler.get_user),
                web.post("/user/create", user_handler.create_user),
                web.put("/user/update/{user_id}", user_handler.update_user),
                web.delete("/user/delete/{user_id}", user_handler.delete_user),

                web.get("/device/get/{device_id}", device_handler.get_device),
                web.post("/device/create", device_handler.create_device),
                web.put("/device/update/{device_id}", device_handler.update_device),
                web.delete("/device/delete/{device_id}", device_handler.delete_device),

                web.get("/location/get/{location_id}", location_handler.get_location),
                web.post("/location/create", location_handler.create_location),
                web.put("/location/update/{location_id}", location_handler.update_location),
                web.delete("/location/delete/{location_id}", location_handler.delete_location)])

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=5050)