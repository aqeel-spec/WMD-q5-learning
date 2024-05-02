from starlette.config import Config
from starlette.datastructures import Secret

# config = Config(".env")

try:
    config = Config(".env.local")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)

TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)

SECRET_KEY = config("SECRET_KEY", cast=Secret)

ALGORITHM = config("ALGORITHM", default="HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=30)

REFRESH_TOKEN_EXPIRE_MINUTES= config("REFRESH_TOKEN_EXPIRE_MINUTES")