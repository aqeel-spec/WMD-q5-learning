# db.py
from typing import  Annotated
from app import settings
from app.model import Todo , User
from sqlmodel import Session, SQLModel, create_engine
from fastapi import  Depends , HTTPException , status

from app.api.dep import SessionDep


connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

# recycle connections after 5 minutes
# to correspond with the compute scale down
engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
# only needed for psycopg 3 - replace postgresql
# with postgresql+psycopg in settings.DATABASE_URL

def get_session():
    with Session(engine) as session:
        yield session

def get_error_404(id : int):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found against {}".format(id))

def get_todo(todo_id : int, session: Annotated[Session, Depends(get_session)]):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise get_error_404(todo_id)
    return todo

def get_user(session : Annotated[Session, Depends(get_session)] , user_id : int):
    user = session.get(User, user_id)
    if not user:
        raise get_error_404(user_id)
    return user



