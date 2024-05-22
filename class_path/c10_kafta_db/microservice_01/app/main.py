# main.py
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from jose import jwt , JWTError

# oAuth2 
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI
from typing import Annotated

from fastapi import HTTPException

# import Todo from sqlmodel
from app.model import Todo , TodoCreate , User , UserCreate
from app import settings
from sqlmodel import  SQLModel, create_engine , Session

# temp
from app.api.main import api_router


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



# The first part of the function, before the yield, will
# be executed before the application starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    
    create_db_and_tables()
    
    print("Tables created!")
    
    yield

    
app : FastAPI = FastAPI(
    lifespan=lifespan,
    title="Creating microservice todo app using FastAPI", 
    version="0.0.1",
    servers=[
        {
            "url": "http://localhost:8002", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
    ]
)

app.include_router(api_router)

# SECRET_KEY = "secret"
# ALGORITHM = "HS256"

# fake_users_db: dict[str, dict[str, str]] = {
#     "ameenalam": {
#         "username": "ameenalam",
#         "full_name": "Ameen Alam",
#         "email": "ameenalam@example.com",
#         "password": "ameenalamsecret",
#     },
#     "aqeel": {
#         "username": "aqeel",
#         "full_name": "Aqeel Shahzad",
#         "email": "aqeel@example.com",
#         "password": "1234",
#     },
# }

# def create_access_token(subject : str , expire_delta : timedelta):
#     expire = datetime.utcnow() + expire_delta
#     to_encode = {"sub": subject, "exp": expire}
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


def get_session():
    with Session(engine) as session:
        yield session
        
# create SessionDep

SessionDep = Annotated[Session, Depends(get_session)]

@app.get("/")
def read_root():
    return {"message": "App is running correctly"}




    

# @app.get("/gen_token")
# def get_token(username : str):
    
#     time = timedelta(minutes = 1)
    
#     token = create_access_token(subject = username, expire_delta = time)
    
#     return {"access_token": token}

# def decoded_token(token:str) : 
#     decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    
#     return decoded_jwt

# @app.get("/decode_token")
# def decode_token(token : str):
    
#     try :
#         decoded_jwt = decoded_token(token)
        
#         # print("expire time of token", decoded_jwt["exp"])
        
#         return {"message": "Token is valid", "decoded_jwt_data": decoded_jwt}
#     except JWTError as e:
#         return {"error" : str(e)}
    
# # create a login api
# @app.post("/login")
# def login(form_data : Annotated[OAuth2PasswordRequestForm, Depends()]):
    
#     """
#     Understanding the login system
#     -> Takes form_data that have username and password
#     """
    
#     # We will add Logic here to check the username/email and password
#     # If they are valid we will return the access token
#     # If they are invalid we will return the error message
#     user_in_db = fake_users_db.get(form_data.username)
    
#     if not user_in_db:
#         raise HTTPException(status_code=400, detail="Incorrect username ")
    
#     if form_data.password != user_in_db["password"]:
#         raise HTTPException(status_code=400, detail="Incorrect password")
    
#     access_token_expires = timedelta(minutes=1)
    
#     access_token = create_access_token(subject=user_in_db["username"], expire_delta=access_token_expires)
    
#     return {"access_token": access_token, "token_type": "bearer", "expires_in": 60}


# # get all users
# @app.get("/users/all")
# def get_all_users():
    
#     return fake_users_db

# # get info login user
# @app.get("/users/me")
# def get_user_me(token : str):
    
#     token_user = decoded_token(token)
    
#     print("token_user", token_user)
    
#     db_user = fake_users_db.get(token_user["sub"])
    
#     return db_user

# command to run uvicorn server
# poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload