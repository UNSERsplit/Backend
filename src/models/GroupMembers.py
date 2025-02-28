from sqlmodel import SQLModel, Field
from typing import Optional

class GroupMembers(SQLModel, table=True):
    memberId: Optional[int] = Field(default=None, primary_key=True)
    userid: int = Field(default=None, foreign_key="user.userid")
    groupid: int = Field(default=None, foreign_key="group.groupid")
    pending: Optional[bool] = False
