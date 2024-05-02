from typing import Annotated

from fastapi import Header, HTTPException , status
from starlette.responses import Response
from fastapi.security import OAuth2PasswordBearer
from ..utils.db import get_session , get_user

from fastapi import Depends , Request
from sqlmodel import Session, select
from passlib.context import CryptContext

from app.model import User , TokenPayload
from app import settings
from typing import Any
from datetime import datetime, timedelta
from jose import jwt , JWTError



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# get db-session and athenticate
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/api/login"
)
refresh_token_scheme = OAuth2PasswordBearer(tokenUrl="/refresh")

SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

# create dummy user having username, email , password
fake_users_db = {
    "johndoe": {
        "username": "aqeel",
        "full_name": "John Doe",
        "email": "aqeel@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password: str):
    return pwd_context.hash(password)
# convert hash password to plain password

    

def get_user_by_email(session : SessionDep, email : str) -> User | None:
    exit_db_user = session.exec(select(User).where(User.email == email)).first()
    return exit_db_user

def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    # expire = datetime.now() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, str(settings.SECRET_KEY), algorithm=settings.ALGORITHM)
    return encoded_jwt

# New function to create refresh token
def create_refresh_token(subject: str | Any, expires_delta: timedelta = None) -> str:
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

def get_current_user(session: SessionDep, token: TokenDep) -> User:
    credentials_exception = creddentials_exception()
    # cookie_token = get_cookies_token(request=Request, key="access_token")
    # print(cookie_token)
    try:
        payload = jwt.decode(
            token, str(settings.SECRET_KEY), algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except JWTError:
        raise credentials_exception
    user = get_user(session, token_data.sub)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    # if not user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def set_cookies_token(response : Response, key : str , value : str):
    res =  response.set_cookie(key=key, value=value, httponly=True)
    return res
def get_cookies_token( request : Request , key : str) -> str:
    cookie_value = request.cookies.get(key)
    return cookie_value

# authorize user with existing token
def athenticated_user(session : SessionDep , email : str , password : str) -> User | None:
    db_user = get_user_by_email(session=session,email=email)
    
    if db_user is None:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
