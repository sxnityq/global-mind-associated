from aiohttp import BasicAuth
from aiohttp.web import middleware, Request, HTTPUnauthorized, HTTPBadRequest
from ..models import UserModel

from hashlib import sha256


@middleware
async def auth_middleware(request: Request, handler):
    if request.rel_url.human_repr() == "/user/create":
        resp = await handler(request)
        return resp
    auth = request.headers.get("Authorization")
    if auth:
        try:
            auth = BasicAuth.decode(auth, encoding="utf-8")
        except Exception as ex:
            return HTTPBadRequest(text="invalid base64 encoding")
        r = UserModel.get(UserModel.name == auth.login)
        if r.password == sha256(auth.password.encode('utf-8')).hexdigest():
            resp = await handler(request)
            return resp
    return HTTPUnauthorized(text="bro u are not allowed to shift this shit") 