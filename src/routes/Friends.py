from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql.functions import current_user

from ..database import DB
from typing import List
from sqlmodel import select
from sqlalchemy import or_, and_
from ..models.Friends import Friends
from ..models.User import User, ShowFriendsAction, PublicUserData
from ..auth import get_current_user
from sqlalchemy import func


friendsRouter = APIRouter(prefix="/api/friends")


@friendsRouter.get("/")
def getAllActiveFriendsOfUser(db: DB, current_user: User = Depends(get_current_user)) -> List[Friends]:
    """get all active Friends, which have accepted the invite"""

    return db.exec(select(Friends).where(and_(or_(current_user.userid == Friends.invited_userid, current_user.userid == Friends.inviting_userid), Friends.pending == False))).all()


@friendsRouter.get("/pending")
def getAllPendingFriendsForUser(db: DB, current_user: User = Depends(get_current_user)) -> List[Friends]:
    """get all pending Friends, which invites you haven't accepted"""

    return db.exec(select(Friends).where(and_(current_user.userid == Friends.invited_userid, Friends.pending == True))).all()

@friendsRouter.get("/users")
def getAllActiveFriendsOfUser(db: DB, current_user: User = Depends(get_current_user)) -> List[PublicUserData]:
    """get all active Friends, which have accepted the invite as User objects"""

    return db.exec(select(User).join(Friends, and_(Friends.pending == False, or_(and_(current_user.userid == Friends.invited_userid, User.userid == Friends.inviting_userid), and_(current_user.userid == Friends.inviting_userid, User.userid == Friends.invited_userid))))).all()


@friendsRouter.get("/search")
def searchActiveFriendsOfUser(db: DB, query: str, current_user: User = Depends(get_current_user)) -> List[PublicUserData]:
    """search active Friends, and return all public user data"""

    query = query.split(" ", maxsplit=1)
    if len(query) == 0:
        raise HTTPException(status_code=400, detail="Invalid query")
    if len(query) == 1:
        return db.exec(select(User).join(Friends, and_(Friends.pending == False, or_(and_(current_user.userid == Friends.invited_userid, User.userid == Friends.inviting_userid), and_(current_user.userid == Friends.inviting_userid, User.userid == Friends.invited_userid)))).where(or_(func.lower(User.firstname + " " + User.lastname).like("%" + query[0].lower() + "%")))).all()
    return db.exec(select(User).join(Friends, and_(Friends.pending == False, or_(and_(current_user.userid == Friends.invited_userid, User.userid == Friends.inviting_userid), and_(current_user.userid == Friends.inviting_userid, User.userid == Friends.invited_userid)))).where(or_(and_(func.lower(User.firstname).like("%" + query[0].lower() + "%"), func.lower(User.lastname).like("%" + query[1].lower() + "%")), and_(func.lower(User.firstname).like("%" + query[1].lower() + "%"), func.lower(User.lastname).like("%" + query[0].lower() + "%"))))).all()




@friendsRouter.post("/")
def sendFriendRequest(db: DB, touserid: int, current_user: User = Depends(get_current_user)) -> Friends:
    if db.exec(select(Friends).where(or_(and_(current_user.userid == Friends.invited_userid, touserid == Friends.inviting_userid), and_(current_user.userid == Friends.inviting_userid, touserid == Friends.invited_userid)))).first() is not None:
        raise HTTPException(status_code=406 , detail="Friend request already sent")
    friendrequest = Friends(invited_userid=touserid, inviting_userid=current_user.userid)
    db.add(friendrequest)
    db.commit()
    db.refresh(friendrequest)

    user = db.exec(select(User).where(User.userid == touserid)).one()
    user.send_message("Neue Freundesanfrage", f"{current_user.firstname} {current_user.lastname} möchte mit die befreundet sein", action=ShowFriendsAction(True))
    
    return friendrequest


@friendsRouter.put("/")
def acceptFriendRequest(db: DB, requestid: int, current_user: User = Depends(get_current_user)):
    friendrequest = db.exec(select(Friends).where(Friends.id == requestid)).one()
    friendrequest.pending = False
    db.commit()
    db.refresh(friendrequest)

    user = db.exec(select(User).where(User.userid == friendrequest.inviting_userid)).one()
    user.send_message("Neuer Freund", f"Du bist nun mit {current_user.firstname} {current_user.lastname} befreundet", action=ShowFriendsAction(False))

    return friendrequest


@friendsRouter.delete("/")
def denyFriendRequest(db: DB, requestid: int, current_user: User = Depends(get_current_user)):
    friendrequest = db.exec(select(Friends).where(Friends.id == requestid)).one()
    db.delete(friendrequest)
    db.commit()
    return friendrequest


@friendsRouter.delete("/{userid}")
def deleteFriend(db: DB, userid: int, current_user: User = Depends(get_current_user)):
    query = db.exec(select(Friends).where(or_(and_(userid == Friends.inviting_userid, current_user.userid == Friends.invited_userid), or_(userid == Friends.invited_userid, current_user.userid == Friends.inviting_userid)))).one()
    db.delete(query)
    db.commit()
    return query
