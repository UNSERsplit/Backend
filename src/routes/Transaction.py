from fastapi import APIRouter, HTTPException, Depends
from ..database import DB
from typing import List
from sqlmodel import select
from sqlalchemy import or_, and_
from ..models.Transaction import Transaction, TransactionCreateRequest
from ..auth import get_current_user
from ..models.User import User
from ..models.Friends import Friends

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
    """create new transaction (only between friends)"""

    transaction = Transaction(**transaction.model_dump(), fromuserid=current_user.userid, date=date.today())
    print(transaction.groupid)
    if db.exec(select(Friends).where(and_(or_(and_(transaction.touserid == Friends.invited_userid, transaction.fromuserid == Friends.inviting_userid), and_(transaction.fromuserid == Friends.invited_userid, transaction.touserid == Friends.inviting_userid)), Friends.pending == False))).one_or_none() is None and transaction.groupid is not None:
        raise HTTPException(status_code=405, detail="Not allowed to invite this user, only friends")

    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction
