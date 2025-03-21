from fastapi import APIRouter, Depends, HTTPException
from ..database import DB
from typing import List
from sqlmodel import select, and_
from ..models.Group import Group, GroupCreationRequest
from ..models.User import User, PublicUserData
from ..models.GroupMembers import GroupMembers
from ..auth import get_current_user

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
def updateGroup(groupid: int, group: GroupCreationRequest, db: DBö) -> Group:
    g = db.exec(select(Group).where(Group.id == groupid)).one()
    g.update(group.model_dump())
    db.commit()
    db.refresh(g)
    return g


"""delete group [ADMIN]"""
@grouprouter.delete("/{groupid}")
def deleteGroup(groupid: int, db: DB) -> Group:
    g = db.exec(select(Group).where(Group.id == groupid)).one()
    db.delete(g)
    db.commit()
    db.refresh(g)
    if db.exec(select(Group)).where(Group.id == groupid):
        raise HTTPException(status_code=500, detail="Group could not be deleted")
    return g


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
def inviteUserToGroup(groupid: int, userid: int, db: DB) -> GroupMembers:  # send invite
    groupmember = GroupMembers(groupid=groupid, userid=userid, pending=True)
    db.add(groupmember)
    db.commit()
    db.refresh(groupmember)
    return groupmember


"""remove user from group [ADMIN]"""
@grouprouter.delete("/{groupid}/users/{userid}")
def deleteUserFromGroup(groupid: int, userid: int, db: DB) -> GroupMembers:
    memberofgroup = db.exec(select(GroupMembers).where(and_(GroupMembers.groupid == groupid, GroupMembers.userid == userid))).one()
    db.delete(memberofgroup)
    db.commit()
    return memberofgroup


"""Get users of Group by Groupid"""
@grouprouter.get("/{groupid}/users")
def getUsersOfGroup(db: DB, groupid: int) -> List[PublicUserData]:
    return db.exec(select(User).join(GroupMembers, User.userid == GroupMembers.userid).where(GroupMembers.groupid == groupid)).all()
