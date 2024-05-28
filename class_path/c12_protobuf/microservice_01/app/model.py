from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


# Define the Todo models for the database

class TodoBase(SQLModel):
    title: str
    description: str
    completed: bool

class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    user_id: int  = Field(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="todos")

class TodoCreate(TodoBase):
    pass

class TodoRead(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

class TodoUpdate(SQLModel):
    title: str | None = None
    completed: bool | None = None
    description: str | None = None
    updated_at: datetime = Field(default=datetime.now())


# Define the User models for the database



class UserBase(SQLModel):
    username: str
    full_name: str
    email: str
    hashed_password: str

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str | None = Field(default=None)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())
    todos: list["Todo"] = Relationship(back_populates="user")
    


class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int 
    created_at: datetime
    updated_at: datetime

class UserUpdate(SQLModel):
    username: str | None = None
    full_name: str | None = None
    email: str | None = None
    hashed_password: str | None = None
    updated_at: datetime = Field(default=datetime.now())


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None