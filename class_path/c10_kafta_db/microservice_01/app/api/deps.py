from typing import Annotated
from fastapi import Depends , status
from sqlmodel import Session
from app.model import User , TokenPayload
from fastapi.security import OAuth2PasswordBearer
from jose import jwt , JWTError
from datetime import timedelta
from app.utils.db import get_user
from fastapi import HTTPException
from app import settings

# temp
from fastapi import Request
from app.utils.db import get_cookies_token

from app.utils.db import get_session


SessionDep = Annotated[Session, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

TokenDep = Annotated[str, Depends(oauth2_scheme)]

refresh_token_scheme = OAuth2PasswordBearer(tokenUrl="/refresh")

# New function to create refresh token
def create_refresh_token(subject: str, expires_delta: timedelta = None) -> str:
    if not expires_delta:
        expires_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(subject), "refresh": True}
    encoded_jwt = jwt.encode(to_encode, str(settings.SECRET_KEY), algorithm=settings.ALGORITHM)
    return encoded_jwt

def creddentials_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception

def decoded_token(token:str) : 
    decoded_jwt = jwt.decode(token, key=str(settings.SECRET_KEY) , algorithms=[settings.ALGORITHM])
    
    print("decoded_jwt",decoded_jwt)
    return decoded_jwt   

# decoded_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTYzOTMwOTAsInN1YiI6IjUifQ.cZ_AviNC9RtISsMfAxk1a3iUQt5P5hRXxI5x37osoBg")

def get_current_user(session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = creddentials_exception()
    # cookie_token = get_cookies_token(request=Request, key="access_token")
    print("token" , token)
    try:
        payload = jwt.decode(
            token, str(settings.SECRET_KEY), algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except JWTError:
        raise credentials_exception
    print("token_data",token_data)
    user = get_user(session, token_data.sub)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    # if not user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

