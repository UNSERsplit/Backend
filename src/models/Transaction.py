from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional
from datetime import date

class TransactionCreateRequest(BaseModel):
    fromuserid: int = Field(default=None, foreign_key="user.userid")
    touserid: int = Field(default=None, foreign_key="user.userid")

    amount: float
    groupid: int = Field(default=None, foreign_key="group.groupid")

class Transaction(SQLModel, TransactionCreateRequest, table=True):
    transactionid: Optional[int] = Field(default=None, primary_key=True)
    date: date