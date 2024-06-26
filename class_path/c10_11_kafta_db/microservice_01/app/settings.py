from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()
    
DATABASE_URL = config("DATABASE_URL", cast=Secret)

TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", int)

SECRET_KEY = config("SECRET_KEY", cast=Secret)
ALGORITHM = config("ALGORITHM", str)


KAFKA_BOOTSTRAP_SERVER=config("KAFKA_BOOTSTRAP_SERVER", str)

KAFKA_ADD_TOPIC=config("KAFKA_ADD_TOPIC", str)

KAFKA_CONSUMER_GROUP_ID_FOR_TODO=config("KAFKA_CONSUMER_GROUP_ID_FOR_TODO", str)