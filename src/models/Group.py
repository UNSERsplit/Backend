from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel

class GroupCreationRequest(BaseModel):
    name: str

class Group(SQLModel, GroupCreationRequest, table=True):
    groupid: Optional[int] = Field(default=None, primary_key=True)
    adminuser_userid: int = Field(default=None, foreign_key="user.userid") # tabellenname automatisch kleingeschrieben
