from sqlmodel import SQLModel, Field
from typing import Optional

class Group(SQLModel, table=True):
    groupid: Optional[int] = Field(default=None, primary_key=True)
    name: str
    adminuser_userid: int = Field(default=None, foreign_key="user.id") # tabellenname automatisch kleingeschrieben
