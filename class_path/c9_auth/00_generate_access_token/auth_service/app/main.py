from fastapi import FastAPI

# creating token and passing values
from jose import JWTError , jwt
from datetime import datetime, timedelta


SECRET_KEY = "secret"
ALGORITHM = "HS256"

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