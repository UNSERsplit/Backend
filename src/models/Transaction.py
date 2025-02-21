from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Transaction(SQLModel, table=True):
    transactionid: Optional[int] = Field(default=None, primary_key=True)
    fromuserid: int = Field(default=None, foreign_key="user.id")
    touserid: int = Field(default=None, foreign_key="user.id")
    date: date
    amount: float
