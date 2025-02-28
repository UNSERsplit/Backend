from fastapi import APIRouter, HTTPException
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
def getUserById(db: DB, userid: int) -> PublicUserData:
    return db.exec(select(User).where(User.userid == userid)).one()


"""register user"""
@userrouter.post("/")
def createUser(user: UserCreateRequest, db: DB) -> User:
    user = User(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


"""update your own data"""
@userrouter.put("/me")
def updateUser(user: UserCreateRequest, db: DB) -> User:
    user = db.exec(select(User)).where(User.id == user.id)
    user.update(**user.model_dump())
    db.commit()
    db.refresh(user)
    return user


"""delete your own account"""
@userrouter.delete("/me")
def deleteUser(user: UserCreateRequest, db: DB) -> str:
    user = db.exec(select(User)).where(User.id == user.id)
    db.delete(user)
    db.commit()
    db.refresh(user)
    if db.execute(select(User)).where(User.id == user.id):
        raise HTTPException(status_code=500, detail="User could not be deleted")
    return user
