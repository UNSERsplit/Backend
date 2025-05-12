from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql.functions import current_user

from ..database import DB
from typing import List
from sqlmodel import select
from sqlalchemy import or_, and_
from ..models.Friends import Friends
from ..models.User import User, ShowFriendsAction
from ..auth import get_current_user

friendsRouter = APIRouter(prefix="/api/friends")


@friendsRouter.get("/")
def getAllActiveFriendsOfUser(db: DB, current_user: User = Depends(get_current_user)) -> List[Friends]:
    """get all active Friends, which have accepted the invite"""

    return db.exec(select(Friends).where(and_(or_(current_user.userid == Friends.invited_userid, current_user.userid == Friends.inviting_userid), Friends.pending == False))).all()


@friendsRouter.get("/pending")
def getAllPendingFriendsForUser(db: DB, current_user: User = Depends(get_current_user)) -> List[Friends]:
    """get all pending Friends, which invites you haven't accepted"""

    return db.exec(select(Friends).where(and_(current_user.userid == Friends.invited_userid, Friends.pending == True))).all()


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
def acceptFriendRequest(db: DB, fromuserid: int, current_user: User = Depends(get_current_user)):
    friendrequest = db.exec(select(Friends).where(and_(fromuserid == Friends.invited_userid, current_user.userid == Friends.inviting_userid))).one()
    friendrequest.pending = False
    db.commit()
    db.refresh(friendrequest)

    user = db.exec(select(User).where(User.userid == fromuserid)).one()
    user.send_message("Neuer Freund", f"Du bist nun mit {current_user.firstname} {current_user.lastname} befreundet", action=ShowFriendsAction(False))

    return friendrequest


@friendsRouter.delete("/")
def denyFriendRequest(db: DB, fromuserid: int, current_user: User = Depends(get_current_user)):
    friendrequest = db.exec(select(Friends).where(and_(fromuserid == Friends.invited_userid, current_user.userid == Friends.inviting_userid))).one()
    db.delete(friendrequest)
    db.commit()
    return friendrequest


@friendsRouter.delete("/{userid}")
def deleteFriend(db: DB, userid: int, current_user: User = Depends(get_current_user)):
    query = db.exec(select(Friends).where(or_(and_(userid == Friends.inviting_userid, current_user.userid == Friends.invited_userid), or_(userid == Friends.invited_userid, current_user.userid == Friends.inviting_userid)))).one()
    db.delete(query)
    db.commit()
    return query
