from fastapi import APIRouter
from ..database import DB
from typing import List
from sqlmodel import select
from ..models.User import User, UserCreateRequest, PrivateUserData


userrouter = APIRouter(prefix="/api/user")


@userrouter.get("/")
def getAllUsers(db: DB) -> List[User]:
    return db.exec(select(User)).all()


@userrouter.get("/{userid}")
def getUserById(db: DB, userid : int) -> User:
    return db.exec(select(User)).where(User.id == userid)


@userrouter.post("/")
def createUser(user: UserCreateRequest) -> bool:
    return 0


@userrouter.put("/{userid}")
def updateUser(user: PrivateUserData) -> PrivateUserData:
    return 0


@userrouter.delete("/{userid}")
def deleteUser() -> str:
    return 0