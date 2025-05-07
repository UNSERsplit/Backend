from fastapi import APIRouter, Depends, HTTPException

from ..database import DB
from typing import List
from sqlmodel import select
from sqlalchemy import or_, and_
from ..models.Group import Group, GroupCreationRequest
from ..models.User import User, PublicUserData, OpenGroupAction
from ..models.GroupMembers import GroupMembers
from ..auth import get_current_user
from ..models.Friends import Friends


grouprouter = APIRouter(prefix="/api/group")


@grouprouter.get("/")
def getAllGroupsOfUser(db: DB, current_user: User = Depends(get_current_user)) -> List[Group]:
    """get all groups i am in"""

    return db.exec(select(Group).join(GroupMembers, Group.groupid == GroupMembers.groupid).where(current_user.userid == GroupMembers.userid)).all()


@grouprouter.get("/{groupid}")
def getGroupByID(groupid: int, db: DB) -> Group:
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
def updateGroup(groupid: int, group: GroupCreationRequest, db: DB, current_user: User = Depends(get_current_user)) -> Group:
    """rename group [ADMIN]"""
    group = db.exec(select(Group).where(Group.groupid == groupid)).one()
    if current_user.userid != group.adminuser_userid:
        raise HTTPException(status_code=403, detail="You are not allowed to invite to this group")
    g = db.exec(select(Group).where(Group.groupid == groupid)).one()
    g.name = group.model_dump()["name"]
    db.commit()
    db.refresh(g)
    return g


@grouprouter.post("/{groupid}/users")
def addUserToGroup(groupid: int, userid: int, db: DB, current_user: User = Depends(get_current_user)) -> GroupMembers:
    """add user to group"""

    groupmember = db.exec(select(GroupMembers).where(and_(groupid == GroupMembers.groupid, userid == GroupMembers.userid))).one()
    groupmember.pending = False
    db.commit()
    db.refresh(groupmember)

    added_user = db.exec(select(User).where(User.userid == userid)).one()
    added_group = db.exec(select(Group).where(Group.groupid == groupid)).one()

    added_user.send_message("Added!", f"{current_user.firstname} added you to '{added_group.name}'", action=OpenGroupAction(groupid))

    return groupmember


@grouprouter.post("/{groupid}/users/{userid}/invite")
def inviteUserToGroup(db: DB, groupid: int, userid: int, current_user: User = Depends(get_current_user)) -> GroupMembers:  # send invite
    """invite user to group [ADMIN]"""
    group = db.exec(select(Group).where(Group.groupid == groupid)).one()
    if db.exec(select(Friends).where(or_(and_(Friends.invited_userid == current_user.userid, Friends.inviting_userid == userid), and_(Friends.invited_userid == userid, Friends.inviting_userid == current_user.userid)))).one_or_none() is None:
        raise HTTPException(status_code=405, detail="Not allowed: Only able to invite friends to group")

    if current_user.userid != group.adminuser_userid:
        raise HTTPException(status_code=403, detail="You are not allowed to invite to this group")
    groupmember = GroupMembers(groupid=groupid, userid=userid, pending=True)
    db.add(groupmember)
    db.commit()
    db.refresh(groupmember)
    return groupmember


@grouprouter.delete("/{groupid}/users/{userid}")
def deleteUserFromGroup(groupid: int, userid: int, db: DB, current_user: User = Depends(get_current_user)) -> GroupMembers:
    """remove user from group [ADMIN]"""
    group = db.exec(select(Group).where(Group.groupid == groupid)).one()
    if current_user.userid != group.adminuser_userid:
        raise HTTPException(status_code=403, detail="You are not allowed to remove users from this group")
    memberofgroup = db.exec(select(GroupMembers).where(and_(GroupMembers.groupid == groupid, GroupMembers.userid == userid))).one()

    removed_user = db.exec(select(User).where(User.userid == userid)).one()
    removed_group = db.exec(select(Group).where(Group.groupid == groupid)).one()

    removed_user.send_message("Removed!", f"you have been removed from '{removed_group.name}'")

    db.delete(memberofgroup)
    db.commit()
    return memberofgroup

@grouprouter.get("/{groupid}/users")
def getUsersOfGroup(db: DB, groupid: int, current_user: User = Depends(get_current_user)) -> List[PublicUserData]:
    """get all users in group [only Groupmembers]"""
    getusers = db.exec(select(GroupMembers).where(and_(GroupMembers.groupid == groupid, GroupMembers.userid == current_user.userid))).all()
    print(getusers)
    if getusers == []:
        raise HTTPException(status_code=403, detail="Not allowed to access this data")
    return db.exec(select(User).join(GroupMembers, User.userid == GroupMembers.userid).where(and_(GroupMembers.groupid == groupid, GroupMembers.pending == False))).all()
