from fastapi import APIRouter, Depends, HTTPException
from ..database import DB
from typing import List
from sqlmodel import select
from ..models.User import User, UserCreateRequest, PrivateUserData, PublicUserData
from ..auth import get_password_hash, get_current_user


userrouter = APIRouter(prefix="/api/user")


# DEBUG
@userrouter.get("/")
def getAllUsers(db: DB) -> List[User]:
    return db.exec(select(User)).all()


"""get public data from User"""
@userrouter.get("/{userid}")
def getUserById(db: DB, userid: int, current_user: User = Depends(get_current_user)) -> PublicUserData:
    return db.exec(select(User).where(User.userid == userid)).one()


"""register user"""
@userrouter.post("/")
def createUser(user: UserCreateRequest, db: DB) -> User:
    user = User.model_validate(user.model_dump(), update={"password":get_password_hash(user.password)})
    db.add(user)
    db.commit()
    db.refresh(user)
    user.password = "-REDACTED-"
    return user

"""get your own data"""
@userrouter.get("/me")
def getSelf(db: DB, current_user: User = Depends(get_current_user)) -> User:
    u = db.exec(select(User)).where(User.id == user.id).one()
    user = User(**u.model_dump())
    user.password = "-REDACTED-"
    return user

"""update your own data"""
@userrouter.put("/me")
def updateUser(user: UserCreateRequest, db: DB, current_user: User = Depends(get_current_user)) -> User:
    u = db.exec(select(User)).where(User.id == user.id).one()
    user.password = u.password
    u.update(**user.model_dump())
    db.commit()
    db.refresh(u)
    user.password = "-REDACTED-"
    return user


"""delete your own account"""
@userrouter.delete("/me")
def deleteUser(user: UserCreateRequest, db: DB, current_user: User = Depends(get_current_user)) -> str:
    user = db.exec(select(User)).where(User.id == user.id).one()
    db.delete(user)
    db.commit()
    db.refresh(user)
    if db.exec(select(User)).where(User.id == user.id):
        raise HTTPException(status_code=500, detail="User could not be deleted")
    user.password = "-REDACTED-"
    return user
