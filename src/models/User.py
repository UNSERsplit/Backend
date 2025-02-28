from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional

class PublicUserData(BaseModel):
    firstname: str
    lastname: str
    iban: Optional[str] = None

class PrivateUserData(BaseModel):
    email: EmailStr = Field(unique=True)
    password: str

class UserCreateRequest(PublicUserData, PrivateUserData):
    pass

class User(SQLModel, UserCreateRequest, table=True):
    userid: Optional[int] = Field(default=None, primary_key=True)