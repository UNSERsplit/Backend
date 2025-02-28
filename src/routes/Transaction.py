from fastapi import APIRouter
from ..database import DB
from typing import List
from sqlmodel import select
from ..models.Transaction import Transaction, TransactionCreateRequest

transactionRouter = APIRouter(prefix="/api/transactions")

"""get all my past transactions"""
@transactionRouter.get("/me")
def getAllTransactionsOfUser() -> List[Transaction]:
    return 0


"""get all transactions between me and other"""
@transactionRouter.get("/to/{touserid}")
def getTransactionsBetweenUsers(touserid: int) -> List[Transaction]:
    return 0

"""create new transaction"""
@transactionRouter.post("/")
def addTransaction(db: DB, transaction: TransactionCreateRequest) -> Transaction:
    return 0


