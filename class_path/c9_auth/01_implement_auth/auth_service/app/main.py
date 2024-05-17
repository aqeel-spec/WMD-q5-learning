from fastapi import FastAPI

# creating token and passing values
from jose import JWTError , jwt
from datetime import datetime, timedelta

# oAuth2 
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from typing import Annotated

from fastapi import HTTPException



SECRET_KEY = "secret"
ALGORITHM = "HS256"

fake_users_db: dict[str, dict[str, str]] = {
    "ameenalam": {
        "username": "ameenalam",
        "full_name": "Ameen Alam",
        "email": "ameenalam@example.com",
        "password": "ameenalamsecret",
    },
    "aqeel": {
        "username": "aqeel",
        "full_name": "Aqeel Shahzad",
        "email": "aqeel@example.com",
        "password": "1234",
    },
}

def create_access_token(subject : str , expire_delta : timedelta):
    expire = datetime.utcnow() + expire_delta
    to_encode = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

app : FastAPI = FastAPI()

@app.get("/")
def read_root():
    return {"message": "App is running correctly"}

@app.get("/gen_token")
def get_token(username : str):
    
    time = timedelta(minutes = 1)
    
    token = create_access_token(subject = username, expire_delta = time)
    
    return {"access_token": token}

def decoded_token(token:str) : 
    decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    
    return decoded_jwt

@app.get("/decode_token")
def decode_token(token : str):
    
    try :
        decoded_jwt = decoded_token(token)
        
        # print("expire time of token", decoded_jwt["exp"])
        
        return {"message": "Token is valid", "decoded_jwt_data": decoded_jwt}
    except JWTError as e:
        return {"error" : str(e)}
    
# create a login api
@app.post("/login")
def login(form_data : Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    """
    Understanding the login system
    -> Takes form_data that have username and password
    """
    
    # We will add Logic here to check the username/email and password
    # If they are valid we will return the access token
    # If they are invalid we will return the error message
    user_in_db = fake_users_db.get(form_data.username)
    
    if not user_in_db:
        raise HTTPException(status_code=400, detail="Incorrect username ")
    
    if form_data.password != user_in_db["password"]:
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    access_token_expires = timedelta(minutes=1)
    
    access_token = create_access_token(subject=user_in_db["username"], expire_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer", "expires_in": 60}


# get all users
@app.get("/users/all")
def get_all_users():
    
    return fake_users_db

# get info login user
@app.get("/users/me")
def get_user_me(token : str):
    
    token_user = decoded_token(token)
    
    print("token_user", token_user)
    
    db_user = fake_users_db.get(token_user["sub"])
    
    return db_user
    
    