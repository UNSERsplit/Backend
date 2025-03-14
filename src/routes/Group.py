from fastapi import APIRouter, Depends, HTTPException
from ..database import DB
from typing import List
from sqlmodel import select
from ..models.Group import Group, GroupCreationRequest
from ..models.User import User, PublicUserData
from ..models.GroupMembers import GroupMembers

grouprouter = APIRouter(prefix="/api/group")

"""get all groups i am in"""
@grouprouter.get("/")
def getAllGroupsOfUser(db: DB, current_user: User = Depends(get_current_user)) -> List[Group]:
    return db.exec(select(Group).join(GroupMembers, Group.groupid == GroupMembers.groupid).where(current_user.userid == GroupMembers.userid)).all()


"""get group"""
@grouprouter.get("/{groupid}")
def getGroupByID(groupid: int, db: DB) -> Group:
    return db.exec(select(Group).where(Group.id == groupid)).one()


"""create group"""
@grouprouter.post("/")
def createGroup(group: GroupCreationRequest) -> Group:
    g = Group(**GroupCreationRequest.model_dump())
    db.add(g)
    db.commit()
    db.refresh(g)
    return g

"""rename group [ADMIN]"""
@grouprouter.put("/{groupid}")
def updateGroup(groupid: int, group: GroupCreationRequest) -> Group:
    return 0

"""delete group [ADMIN]"""
@grouprouter.delete("/{groupid}")
def deleteGroup(groupid: int) -> str:
    return 0

"""add user to group [ADMIN]"""
@grouprouter.post("/{groupid}/users")
def addUserToGroup(groupid: int, userid: int, db: DB) -> GroupMembers:  # accepted invite and admin accepts user
    groupmember = db.exec(select(GroupMembers).where(and_(groupid == GroupMembers.groupid,userid == GroupMembers.userid))).one()
    groupmember.update(pending=False)
    db.commit()
    db.refresh(groupmember)
    return groupmember


"""invite user to group"""
@grouprouter.post("/{groupid}/users/{userId}/invite")
def inviteUserToGroup(groupid: int, userid: int) -> GroupMembers:  # send invite
    groupmember = GroupMembers(groupid=groupid, userid=userid, pending=True)
    db.add(groupmember)
    db.commit()
    db.refresh(groupmember)
    return groupmember


"""remove user from group [ADMIN]"""
@grouprouter.delete("/{groupid}/users/{userid}")
def deleteUserFromGroup(groupid : int, userid: int) -> str:
    return 0

@grouprouter.get("/{groupid}/users")
def getUsersOfGroup(db: DB, groupid: int) -> List[PublicUserData]:
    return db.exec(select(User).join(GroupMembers, User.userid == GroupMembers.userid).where(GroupMembers.groupid == groupid)).all()
