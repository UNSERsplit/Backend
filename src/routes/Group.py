from fastapi import APIRouter
from ..database import DB
from typing import List
from sqlmodel import select
from ..models.Group import Group, GroupCreationRequest

grouprouter = APIRouter(prefix="/api/group")

"""get all groups i am in"""
@grouprouter.get("/")
def getAllGroups() -> List[Group]:
    return 0

"""get group"""
@grouprouter.get("/{groupid}")
def getGroupByID(groupid: int) -> Group:
    return 0

"""create group"""
@grouprouter.post("/")
def createGroup(group: GroupCreationRequest) -> Group:
    return 0

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
def addUserToGroup(groupid: int, userId: int) -> str:  # accepted invite and admin accepts user
    return 0

"""invite user to group"""
@grouprouter.post("/{groupid}/users/{userId}/invite")
def inviteUserToGroup(groupsid: int, userId: int) -> str:  # send invite
    return 0

"""remove user from group [ADMIN]"""
@grouprouter.delete("/{groupid}/users/{userid}")
def deleteUserFromGroup(groupid : int, userid: int) -> str:
    return 0