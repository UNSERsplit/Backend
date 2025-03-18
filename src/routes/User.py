from fastapi import APIRouter, Depends, HTTPException
from ..database import DB
from typing import List
from sqlmodel import select
from ..models.User import User, UserCreateRequest, PrivateUserData, PublicUserData
from ..auth import get_password_hash, get_current_user


userrouter = APIRouter(prefix="/api/user")


@userrouter.get("/{userid}")
def getUserById(db: DB, userid: int, _: User = Depends(get_current_user)) -> PublicUserData:
    """get public data from User"""

    return db.exec(select(User).where(User.userid == userid)).one()


@userrouter.post("/")
def createUser(user: UserCreateRequest, db: DB) -> User:
    """register user"""

    user = User.model_validate(user.model_dump(), update={"password":get_password_hash(user.password)})
    db.add(user)
    db.commit()
    db.refresh(user)
    user.password = "-REDACTED-"
    return user

@userrouter.get("/me")
def getSelf(db: DB, current_user: User = Depends(get_current_user)) -> User:
    """get your own data"""

    u = db.exec(select(User)).where(User.id == current_user.id).one()
    user = User(**u.model_dump())
    user.password = "-REDACTED-"
    return user

@userrouter.put("/me")
def updateUser(user: UserCreateRequest, db: DB, current_user: User = Depends(get_current_user)) -> User:
    """update your own data"""

    u = db.exec(select(User)).where(User.id == current_user.id).one()
    user.password = u.password
    u.update(**user.model_dump())
    db.commit()
    db.refresh(u)
    user.password = "-REDACTED-"
    return user


@userrouter.delete("/me")
def deleteUser(user: UserCreateRequest, db: DB, current_user: User = Depends(get_current_user)) -> str:
    """delete your own account"""
    
    user = db.exec(select(User)).where(User.id == current_user.id).one()
    db.delete(user)
    db.commit()
    db.refresh(user)
    if db.exec(select(User)).where(User.id == current_user.id):
        raise HTTPException(status_code=500, detail="User could not be deleted")
    user.password = "-REDACTED-"
    return user
