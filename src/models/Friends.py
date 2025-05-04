from sqlmodel import SQLModel, Field
from typing import Optional

class Friends(SQLModel, table=True):
    __tablename__ = "friends"
    id: Optional[int] = Field(default=None, primary_key=True)
    inviting_userid: int = Field(default=None, foreign_key="user.userid")
    invited_userid: int = Field(default=None, foreign_key="user.userid")
    pending: Optional[bool] = True