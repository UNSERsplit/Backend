from fastapi import APIRouter, Depends, HTTPException
from ..database import DB
from typing import List
from sqlmodel import select, and_
from ..models.Group import Group, GroupCreationRequest
from ..models.User import User, PublicUserData
from ..models.GroupMembers import GroupMembers
from ..auth import get_current_user

grouprouter = APIRouter(prefix="/api/group")

@grouprouter.get("/")
def getAllGroupsOfUser(db: DB, current_user: User = Depends(get_current_user)) -> List[Group]:
    """get all groups i am in"""

    return db.exec(select(Group).join(GroupMembers, Group.groupid == GroupMembers.groupid).where(current_user.userid == GroupMembers.userid)).all()


@grouprouter.get("/{groupid}")
def getGroupByID(groupid: int, db: DB, current_user: User = Depends(get_current_user)) -> Group:
    """get group"""

    return db.exec(select(Group).where(Group.groupid == groupid)).one()


@grouprouter.post("/")
def createGroup(db: DB, group: GroupCreationRequest, current_user: User = Depends(get_current_user)) -> Group:
    """create group"""

    g = Group(**group.model_dump(), adminuser_userid=current_user.userid)
    db.add(g)
    db.commit()
    db.refresh(g)

    groupmember = GroupMembers(groupid=g.groupid, userid=current_user.userid, pending=False)
    db.add(groupmember)
    db.commit()
    db.refresh(groupmember)
    return g

@grouprouter.put("/{groupid}")
def updateGroup(groupid: int, group: GroupCreationRequest, current_user: User = Depends(get_current_user)) -> Group:
    """rename group [ADMIN]"""

    return 0

@grouprouter.delete("/{groupid}")
def deleteGroup(groupid: int, current_user: User = Depends(get_current_user)) -> str:
    """delete group [ADMIN]"""

    return 0

@grouprouter.post("/{groupid}/users")
def addUserToGroup(groupid: int, userid: int, db: DB, current_user: User = Depends(get_current_user)) -> GroupMembers:  # accepted invite and admin accepts user
    """add user to group [ADMIN]"""

    groupmember = db.exec(select(GroupMembers).where(and_(groupid == GroupMembers.groupid,userid == GroupMembers.userid))).one()
    groupmember.update(pending=False)
    db.commit()
    db.refresh(groupmember)
    return groupmember


@grouprouter.post("/{groupid}/users/{userid}/invite")
def inviteUserToGroup(db: DB, groupid: int, userid: int, current_user: User = Depends(get_current_user)) -> GroupMembers:  # send invite
    """invite user to group"""

    groupmember = GroupMembers(groupid=groupid, userid=userid, pending=True)
    db.add(groupmember)
    db.commit()
    db.refresh(groupmember)
    return groupmember


@grouprouter.delete("/{groupid}/users/{userid}")
def deleteUserFromGroup(groupid : int, userid: int, current_user: User = Depends(get_current_user)) -> str:
    """remove user from group [ADMIN]"""

    return 0

@grouprouter.get("/{groupid}/users")
def getUsersOfGroup(db: DB, groupid: int, current_user: User = Depends(get_current_user)) -> List[PublicUserData]:
    """get all users in group"""
    return db.exec(select(User).join(GroupMembers, User.userid == GroupMembers.userid).where(and_(GroupMembers.groupid == groupid, GroupMembers.pending == False))).all()
