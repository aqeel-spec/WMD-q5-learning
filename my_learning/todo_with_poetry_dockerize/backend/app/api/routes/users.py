# users.py , user

from app.model import User , UserCreate , UserUpdate
from sqlmodel import select
from fastapi import APIRouter
from app.api.dep import SessionDep , CurrentUser 

from app.utils.db import   get_error_404 , get_user 
# from jose import JWTError , jwt
from passlib.context import CryptContext


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/api/user/register", response_model=User)
def create_new_user(session : SessionDep, create_user : UserCreate):
    db_user = User.model_validate(create_user,update={"hashed_password": get_password_hash(create_user.hashed_password)})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user




@router.get("/api/users", response_model=list[User])
def all_registred_users(session : SessionDep , currentUser:CurrentUser):
    users = session.exec(select(User)).all()
    if not users:
        raise get_error_404
    return users

@router.get("/api/users/{email}")
def Get_user_by_email(email : str, session : SessionDep):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise get_error_404
    return user


@router.get("/api/users/me/", response_model=User)
async def read_users_me( current_user: CurrentUser):
    return current_user

@router.get("/api/user/{user_id}", response_model=User)
def get_db_user(session : SessionDep,currentUser:CurrentUser, user_id : int):
    db_user = session.get(User, user_id)
    if not db_user:
        raise get_error_404
    return db_user


@router.put("/user/{user_id}", response_model=User)
def update_user(session : SessionDep, currentUser:CurrentUser ,user_id : int, user : UserUpdate):
    db_user = get_user(session, user_id)
    if not db_user:
        raise get_error_404
    changed_data = user.model_dump(exclude_unset=True)
    for key, value in changed_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/user/{user_id}")
def delete_user(session: SessionDep,currentUser:CurrentUser,user_id: int):
    db_user = session.get(User, user_id)
    if not db_user:
        raise get_error_404
    
    session.delete(db_user)
    session.commit()
    return db_user

