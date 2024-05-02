from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from app.api.dep import SessionDep, creddentials_exception
from app.model import Token , User, TokenPayload
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request


from app.settings import  ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY , ALGORITHM
from jose import JWTError , jwt
from app.api.dep import create_access_token , athenticated_user , fake_users_db , set_cookies_token, get_cookies_token, verify_password



router = APIRouter()



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
TokenDep = Annotated[str, Depends(oauth2_scheme)]    


@router.post("/api/login")
def login_access_token(response : Response, session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) :
    
    
    user = athenticated_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # return user.id
    token = Token(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
    # wait to save the created token in browser cookie
    
    if token is not None: 
        set_cookies_token(response=response, key="access_token", value=token.access_token)
        return token
    else:
        raise HTTPException(status_code=400, detail="Incorrect email or password")


# @router.get("/cookie-token")
# def access_token(request : Request) :
#     token = get_cookies_token(request=request, key="access_token")
#     return token

# athenticate user with existing token in cookies
@router.post("/cookie-token-user")
def access_token_user(response : Response) :
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {"message": "Come to the dark side, we have cookies"}