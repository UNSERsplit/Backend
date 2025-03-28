from fastapi import APIRouter, HTTPException, Depends
from ..database import DB
from typing import List
from sqlmodel import select
from ..models.User import User, UserCreateRequest, PrivateUserData, PublicUserData
from ..auth import get_password_hash, get_current_user


userrouter = APIRouter(prefix="/api/user")


@userrouter.get("/")
def getUsers(db: DB) -> List[User]:
    """Get all User data"""
    return db.exec(select(User)).all()


@userrouter.get("/{userid:int}")
def getUserById(db: DB, userid: int, _: User = Depends(get_current_user)) -> PublicUserData:
    """get public data from User"""

    return db.exec(select(User).where(User.userid == userid)).one()


@userrouter.post("/")
def createUser(user: UserCreateRequest, db: DB) -> User:
    """register user"""

    user = User.model_validate(user.model_dump(), update={"password": get_password_hash(user.password)})
    db.add(user)
    db.commit()
    db.refresh(user)
    user.password = "-REDACTED-"
    return user

@userrouter.get("/me")
def getSelf(db: DB, current_user: User = Depends(get_current_user)) -> User:
    """get your own data"""

    u = db.exec(select(User).where(User.userid == current_user.userid)).one()
    user = User(**u.model_dump())
    user.password = "-REDACTED-"
    return user

@userrouter.put("/me")
def updateUser(user: UserCreateRequest, db: DB, current_user: User = Depends(get_current_user)) -> User:
    """update your own data"""
    u = db.exec(select(User).where(User.userid == current_user.userid)).one()
    u.firstname = user.firstname
    u.lastname = user.lastname
    u.iban = user.iban
    u.password = get_password_hash(user.password)
    db.commit()
    db.refresh(u)
    u.password = "-REDACTED-"
    return u


@userrouter.delete("/me")
def deleteUser(db: DB, current_user: User = Depends(get_current_user)) -> User:
    """delete your own account"""

    user = db.exec(select(User).where(User.userid == current_user.userid)).one()
    db.delete(user)
    db.commit()
    user.password = "-REDACTED-"
    return user
