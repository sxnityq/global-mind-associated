from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

DB_NAME=getenv("PG_DB")
DB_PASS=getenv("PG_PASS")
DB_USER=getenv("PG_USER")
DB_PORT=getenv("PG_PORT", default=5432)
DB_HOST=getenv("PG_HOST", default="0.0.0.0")