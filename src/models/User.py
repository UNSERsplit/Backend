from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional

class _PublicUserData(BaseModel):
    firstname: str
    lastname: str
    iban: Optional[str] = None

class PublicUserData(_PublicUserData):
    userid: Optional[int] = Field(default=None, primary_key=True)

class PrivateUserData(BaseModel):
    email: EmailStr = Field(unique=True)
    password: str

class UserCreateRequest(_PublicUserData, PrivateUserData):
    pass

class User(SQLModel, UserCreateRequest, PublicUserData, table=True):
    pass