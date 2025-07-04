from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str

class UserPublic(SQLModel):
    id: int 
    username: str

class UserCreate(SQLModel):
    username: str
    password: str

class AppOwner(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
