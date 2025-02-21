from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import Optional

class User(SQLModel, table=True):
    userid: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    firstname: str
    lastname: str
    iban: Optional[str] = None
    password: str
