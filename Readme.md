# What's Up 👋

This is my test assignment in Global Mind Associated. The main goal was to create async REST api for managing user, device and location tables.
During process I faced issue with Auth method choice. Aiohttp is very simplified framework so it only provides Basic Auth method.
This is not secure ofc but I have used it only because I was really cut off in time. Theoretically, if I had more time, I would implement jwt with.

## How to run ?

1. create .env file in the root directory. Is is really important to name it ".env" because I use exactly the same name as --env-file param for containerised run and use it to load envs via dotenv.

here u can copy/paste my .env file for simplicity

- PG_USER="Geralt"
- PG_PASS="secret_as_fuck"
- PG_DB="mydb"
- PG_HOST="postgres"
- PG_PORT=5432
- PGADM_PASS="secret_as_fuck2"
- PGADM_EMAIL="terrydevis@cia.slander"

2.  run docker-compose file that create pgadmin, postgres and app containers.
    CAUTION! pgadmin and postgres services create pgadmin4/pgdata bind mount folders in root directory.

```bash
docker-compose up -d
```

3. use curl for quering endpoints.

```bash
curl -X <method> <url> -H Authorization: Basic <base64 token> -d <json data>
```

## Structure 💾

`````.
├── code
│   ├── config.py -> contains some sort of config params.  Like database arguments
│   ├── database.py -> database connection instance
│   ├── handlers -> request handlers
|   ├── middlewares -> auth middleware
│   ├── models -> database orm models
│   ├── schemas -> Pydantic models to validate data
│   └── utils -> useful utilities like base64 generator
├── docker-compose.yml
├── Dockerfile
├── main.py -> main file
├── Readme.md
└── requirements.txt````
`````

## Base usage

#### Create user

`curl -X POST http://0.0.0.0:5050/user/create -H "Content-Type: application/json" -d '{"name": "protein bar", "email": "theking@sportstyle.com", "password":"Iusearchbtw1^&)"}'`

response -> `cHJvdGVpbiBiYXI6SXVzZWFyY2hidHcxXiYp`

Now with this token we can use other api methods. I have created auth middleware that validates HTTP "Authorization" header to possibilities hit specified endpoint.
Basicaly it fetch base64 token from header and decode it. Then it selects by login (name unique field) user model and verifies that provided sha256 hashed password is correct

```python
try:
    auth = BasicAuth.decode(auth, encoding="utf-8")
    except Exception as ex:
        return HTTPBadRequest(text="invalid base64 encoding")
    r = UserModel.get(UserModel.name == auth.login)
    if r.password == sha256(auth.password.encode('utf-8')).hexdigest():
```

It is complicated, but that is the problem of Basic Auth. With JWT it would be much easier and faster.

#### Now let's use token 🎫

`curl -X GET http://0.0.0.0:5050/user/get/18 -H "Content-Type: application/json" -H "Authorization: Basic cHJvdGVpbiBiYXI6SXVzZWFyY2hidHcxXiYp"`
response -> {"name": "protein bar", "email": "theking@sportstyle.com", "devices": []}

As we can see our user doesn't have devices. Let's create one. (Btw in example id is 18 cause I quering at existing databases with pre tested rows, my fault xD)

#### create devices and location 👨🏻‍💻

First of all we have to create location or use existing one. For simplicity I will create one so don't worry.

`curl -X POST http://0.0.0.0:5050/location/create -H "Content-Type: application/json" -H "Authorization: Basic cHJvdGVpbiBiYXI6SXVzZWFyY2hidHcxXiYp" -d '{"name": "secret as fuck"}'`

response - > 201: location with id 3 was successfully created

Anyway lets move forward to create our device.

`curl -X POST http://0.0.0.0:5050/device/create -H "Content-Type: application/json" -H "Authorization: Basic cHJvdGVpbiBiYXI6SXVzZWFyY2hidHcxXiYp" -d '{"name": "very awesome shrink ray", "location_id": 3, "type": "moon stiller", "login" : "despicable me 1", "password" : "Verysecretspy#1488)"}'`

response -> device with id 4 was created

#### Aaaaaaand Let's fetch our homie again

`curl -X GET http://0.0.0.0:5050/user/get/18 -H "Content-Type: application/json" -H "Authorization: Basic cHJvdGVpbiBiYXI6SXVzZWFyY2hidHcxXiYp" `

response -> {"name": "protein bar", "email": "theking@sportstyle.com", "devices": [{"id": 4, "name": "very awesome shrink ray", "device_type": "moon stiller", "login": "despicable me 1", "location_id": 3, "api_user_id": 18}]}

Now we can see our new device is inside devices list. Cool? Cool as fuck (⌐■_■)

#### delete device

Well only by losing everything do we gain freedom. Let's clean up shrink tay

`curl -X DELETE http://0.0.0.0:5050/device/delete/4  -H "Content-Type: application/json" -H "Authorization: Basic cHJvdGVpbiBiYXI6SXVzZWFyY2hidHcxXiYp" `

Ang get user again)

`curl -X GET http://0.0.0.0:5050/user/get/18 -H "Content-Type: application/json" -H "Authorization: Basic cHJvdGVpbiBiYXI6SXVzZWFyY2hidHcxXiYp"`

response - > {"name": "protein bar", "email": "theking@sportstyle.com", "devices": []}

![](https://github.com/sxnityq/global-mind-associated/blob/main/readmeSrc/end.gif)
