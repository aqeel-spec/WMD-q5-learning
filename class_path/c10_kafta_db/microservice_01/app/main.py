# main.py
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from typing import Annotated
from app import settings
from sqlmodel import  SQLModel, create_engine , Session

# temp
from app.api.main import api_router

# aiokafka messages
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio



# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)
engine = create_engine(
    connection_string,
    connect_args={"sslmode": "disable"},
    pool_recycle=300
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    

        
async def consumer_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic, # we may have multiple topics
        bootstrap_servers=bootstrap_servers,
        group_id="my-group",
        auto_offset_reset="earliest",
    )
    
    await consumer.start()

    try:
        async for msg in consumer:
            print(f"Received message: {msg.value.decode()} on topic {msg.topic}")
            # Do something with the message
            # Example : Save it to a database
    finally:
        # Close down the consumer
        await consumer.stop()

# The first part of the function, before the yield, will
# be executed before the application starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    
    create_db_and_tables()
    
    print("Tables created!")
    
    # loop.run_until_complete(consume_messages('todos', 'broker:19092'))
    task = asyncio.create_task(consumer_messages('todo', 'broker:19092'))
    
    yield

    
app : FastAPI = FastAPI(
    lifespan=lifespan,
    title="Creating microservice todo app using FastAPI", 
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
    ]
)

app.include_router(api_router)


def get_session():
    with Session(engine) as session:
        yield session
        
# create SessionDep

SessionDep = Annotated[Session, Depends(get_session)]

@app.get("/")
def read_root():
    return {"message": "App is running correctly"}


# command to run uvicorn server
# poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload