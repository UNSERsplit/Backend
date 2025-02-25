from fastapi import APIRouter
from ..database import DB
from typing import List
from sqlmodel import select
from ..models.User import User


userrouter = APIRouter(prefix="/api/user")


@userrouter.get("/")
def getAllUsers(db: DB) -> List[User]:
    return db.exec(select(User)).all()


@userrouter.get("/{userid}")
def getUserById(db: DB, userid : int) -> User:
    return db.exec(select(User)).where(User.id == userid)


@userrouter.post("/")
def createUser(user: User):
    return 0


@userrouter.put("/{userid}")
def updateUser(user: User):
    return 0


@userrouter.delete("/{userid}")
def deleteUser(user: User):
    return 0

@userrouter.put("/resetpassword/{userid}")
def resetPassword(userid: int, password: str):
    return 0

@userrouter.get("/resetpassword/{userid}")
def getResetPassword(userid: int, password: str):
    return 0