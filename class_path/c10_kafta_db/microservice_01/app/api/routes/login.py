from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from app.api.deps import SessionDep
from fastapi import Depends
from fastapi import Response
from typing import Annotated
from app.utils.db import  athenticate_user , create_access_token , create_cookies_token
from app import settings
from datetime import timedelta

from app.model import Token , User, TokenPayload

# temp
from fastapi import HTTPException 

router = APIRouter()

# create auth scheme and procide your api login path

# function to create access token


@router.post("/login")
def login(response : Response ,  session : SessionDep,form_data : Annotated[OAuth2PasswordRequestForm, Depends()]):
    # get user from email
    user = athenticate_user(session=session, email=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # access token expires in
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # create access token
    token = Token(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
    
    # save the created token in browser cookie
    create_cookies_token(response=response, key="access_token", value=token.access_token)
    
    return {"token": token, "expires_in": access_token_expires}
    
    
    