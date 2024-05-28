from fastapi import APIRouter , HTTPException , status

from app.api.deps import SessionDep , CurrentUser
from app.model import User, UserCreate, UserUpdate
from sqlmodel import  select
from app.utils.db import get_user_404_error , get_user


router = APIRouter()




# register user in database
@router.post("/register", response_model=User)
def create_new_user(session : SessionDep, create_user : UserCreate):
    db_user = User.from_orm(create_user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/users/me/", response_model=User)
def read_users_me( current_user: CurrentUser ):
    return current_user

@router.get("/users", response_model=list[User])
def all_registred_users(session : SessionDep , currentUser:CurrentUser):
    users = session.exec(select(User)).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found")
    return users

# get user by id
@router.get("/users/{user_id}", response_model=User)
def get_db_user(session : SessionDep, user_id : int, current_user : CurrentUser ):
    db_user = session.get(User, user_id)
    if not db_user:
        # this is hard coded id when we get current user it will get this id automatically
        # -> raise get_user_404_error
        raise get_user_404_error(user_id)
    return db_user

@router.put("/user/{user_id}", response_model=User)
def update_user(session : SessionDep ,user_id : int, user : UserUpdate, current_user : CurrentUser ):
    db_user = get_user(session, user_id)
    if not db_user:
        raise get_user_404_error(user_id)
    changed_data = user.model_dump(exclude_unset=True)
    for key, value in changed_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/user/{user_id}")
def delete_user(session: SessionDep , user_id: int , current_user : CurrentUser ):
    db_user = session.get(User, user_id)
    if not db_user:
        raise get_user_404_error(user_id)
    
    session.delete(db_user)
    session.commit()
    return {
        "message" : "User deleted successfully",
        "deleted_user" : db_user.model_dump()
    }