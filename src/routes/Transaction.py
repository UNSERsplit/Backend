from fastapi import APIRouter, HTTPException, Depends
from ..database import DB
from typing import List
from sqlmodel import select
from sqlalchemy import or_, and_
from ..models.Transaction import Transaction, TransactionCreateRequest
from ..auth import get_current_user
from ..models.User import User

from datetime import date

transactionRouter = APIRouter(prefix="/api/transactions")

@transactionRouter.get("/me")
def getAllTransactionsOfUser(db: DB, current_user: User = Depends(get_current_user)) -> List[Transaction]:
    """get all my past transactions"""

    return db.exec(select(Transaction).where(or_(Transaction.fromuserid == current_user.userid, Transaction.touserid == current_user.userid))).all()


@transactionRouter.get("/to/{touserid}")
def getTransactionsBetweenUsers(touserid: int, db: DB, current_user: User = Depends(get_current_user)) -> List[Transaction]:
    """get all transactions between me and other"""

    return db.exec(select(Transaction).where(or_(and_(Transaction.fromuserid == current_user.userid, Transaction.touserid == touserid), and_(Transaction.fromuserid == touserid, Transaction.touserid == current_user.userid)))).all()


@transactionRouter.post("/")
def addTransaction(db: DB, transaction: TransactionCreateRequest, current_user: User = Depends(get_current_user)) -> Transaction:
    """create new transaction"""

    transaction = Transaction(**transaction.model_dump(), fromuserid=current_user.userid, date=date.today())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


