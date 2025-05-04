from fastapi import APIRouter, HTTPException, Depends
from ..database import DB
from typing import List
from sqlmodel import select, and_
from sqlalchemy import func
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

@userrouter.get("/search")
def searchUsers(db: DB, query: str, _: User = Depends(get_current_user)) -> List[PublicUserData]:
    """get public data from User that matches query"""

    query = query.split(" ", maxsplit=1)
    if len(query) == 1:
        return db.exec(select(User).where(func.lower(User.firstname).like(query[0].lower() + "%"))).all()
    else:
        return db.exec(select(User).where(and_(func.lower(User.firstname).like(query[0].lower()), User.lastname.like(query[1].lower() + "%")))).all()

@userrouter.post("/")
def createUser(user: UserCreateRequest, db: DB) -> User:
    """register user"""
    if user.iban is not None:
        isIbanValid(user.iban)
        raise HTTPException("Iban not valid")
        return null;
    user = User.model_validate(user.model_dump(), update={"password": get_password_hash(user.password)})
    db.add(user)
    db.commit()
    db.refresh(user)
    user.password = "-REDACTED-"
    return user


def convertCharsToNumbers(string):
    new = ""
    string_chararray = [char for char in string.upper()]
    for c in string_chararray:
        if '0' <= c <= '9':
            new = new + c
        else:
            value = ord(c) -  ord('A') + 10
            new = new + str(value)
    return int(new)


def isIbanValid(iban: str) -> bool:
    if iban is None:
        return True
    spacelessiban = iban.replace(" ", "").strip()
    if len(spacelessiban) != 20:
        return False
    if spacelessiban[:2] != "AT":
        return False

    movediban = spacelessiban[4:] + spacelessiban[:4];
    print(movediban)
    asinteger = convertCharsToNumbers(movediban)
    print(asinteger)
    mod = asinteger % 97
    print(mod)
    if mod == 1:
        return True
    else:
        return False


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
    if user.iban is not None:
        isIbanValid(user.iban)
        raise HTTPException("Iban not valid")
        return null;
    u = db.exec(select(User).where(User.userid == current_user.userid)).one()
    u.firstname = user.firstname
    u.lastname = user.lastname
    u.iban = user.iban
    u.password = get_password_hash(user.password)
    db.commit()
    db.refresh(u)
    u.password = "-REDACTED-"
    return u

@userrouter.post("/device_token")
def updateUser(device_token: str, db: DB, current_user: User = Depends(get_current_user)) -> User:
    """update your own fcm device token"""
    u = db.exec(select(User).where(User.userid == current_user.userid)).one()
    u.fcm_device_token = device_token
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
