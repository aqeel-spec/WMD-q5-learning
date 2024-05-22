# main.py
from contextlib import asynccontextmanager
from typing import Union, Optional, Annotated
from app import settings
from sqlmodel import Field, Session, SQLModel, create_engine, select, Sequence
from fastapi import FastAPI, Depends
from typing import AsyncGenerator

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(index=True)

connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)

try:
    # Ping the database
    is_connected = engine.connect()
    # print("Database connection successful.",is_connected)
    if is_connected:
        print("Database connection is active.")
    else:
        print("Database connection failed.")
except Exception as e:
    print(f"Error checking connection: {e}")


# The first part of the function, before the yield, will
# be executed before the application starts
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Creating tables..")
#     create_db_and_tables()
#     yield


app : FastAPI= FastAPI(
    # lifespan=lifespan,
    title="Todo with FastAPI and Docker", 
    version="0.0.1",
    servers=[
        {
            "url": "http://localhost:8000", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])

def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
def read_root():
    return {"Class_05": "Docker with FastAPI"}

@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo, session: Annotated[Session, Depends(get_session)])->Todo:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo


@app.get("/todos/", response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)]):
        todos = session.exec(select(Todo)).all()
        return todos