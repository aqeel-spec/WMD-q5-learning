from sqlmodel import  create_engine, Session
from app import settings
from fastapi import  HTTPException , status , Response , Request
from typing import Annotated 
from app.model import User
from fastapi import Depends
from sqlmodel import select , Session
from jose import jwt
# from app.api.deps import SessionDep
from datetime import timedelta , datetime


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

def get_session():
    with Session(engine) as session:
        yield session
        
def get_user(session : Annotated[Session, Depends(get_session)] , user_id : int):
    user = session.get(User, user_id)
    if not user:
        raise get_user_404_error(user_id)
    return user

def get_user_by_email(session : Annotated[Session, Depends(get_session)], email : str) -> User | None:
    exit_db_user = session.exec(select(User).where(User.email == email)).first()
    return exit_db_user
    
def get_user_404_error(id : int):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found against {}".format(id))

def athenticate_user(session : Annotated[Session, Depends(get_session)], email : str, password : str):
    # get user from email
    db_user = get_user_by_email(session=session,email=email)
    
    # Check user and password against database
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found against this email")
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect email")
    elif password != db_user.hashed_password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
    
    # returning database user if email and password is correct
    return db_user
    
def create_access_token(subject: str, expires_delta: timedelta) -> str:
    
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    # expire = datetime.now() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, str(settings.SECRET_KEY), algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_cookies_token(response : Response, key : str , value : str):
    response.set_cookie(key=key, value=value, httponly=True)
    return response

def get_cookies_token( request : Request , key : str) -> str:
    cookie_value = request.cookies.get(key)
    return cookie_value