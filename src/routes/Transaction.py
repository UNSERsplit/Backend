from fastapi import APIRouter
from ..database import DB
from typing import List
from sqlmodel import select
from ..models.Transaction import Transaction

transactionRouter = APIRouter(prefix="/api/transactions")

@transactionRouter.get("/{userid}")
def getAllTransactionsOfUser(userid: int) -> List[Transaction]:
    return 0


@transactionRouter.get("/to/{touserid}")
def gettTransactionsBetweenUsers(touserid: int) -> List[Transaction]:
    return 0


@transactionRouter.post("/")
def addTransaction(db: DB, transaction: Transaction):
    return 0


