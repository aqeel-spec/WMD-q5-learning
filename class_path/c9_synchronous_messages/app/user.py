from sqlmodel import Field, SQLModel

class User(SQLModel):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)