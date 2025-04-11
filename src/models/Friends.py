from sqlmodel import SQLModel, Field
from typing import Optional

class Friends(SQLModel, table=True):
    inviting_userid: int = Field(default=None, foreign_key="user.userid")
    invited_userid: int = Field(default=None, foreign_key="user.userid")
    pending: Optional[bool] = False