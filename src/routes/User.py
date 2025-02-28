from fastapi import APIRouter
from ..database import DB
from typing import List
from sqlmodel import select
from ..models.User import User, UserCreateRequest, PrivateUserData, PublicUserData


userrouter = APIRouter(prefix="/api/user")

# DEBUG
@userrouter.get("/")
def getAllUsers(db: DB) -> List[User]:
    return db.exec(select(User)).all()

"""get public data from User"""
@userrouter.get("/{userid}")
def getUserById(db: DB, userid : int) -> PublicUserData:
    return db.exec(select(User)).where(User.id == userid)


"""register user"""
@userrouter.post("/")
def createUser(user: UserCreateRequest) -> User:
    return 0

"""update your own data"""
@userrouter.put("/me")
def updateUser(user: UserCreateRequest) -> User:
    return 0

"""delete your own account"""
@userrouter.delete("/me")
def deleteUser() -> str:
    return 0