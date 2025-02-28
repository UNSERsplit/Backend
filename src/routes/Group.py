from fastapi import APIRouter
from ..database import DB
from typing import List
from sqlmodel import select
from ..models.Group import Group, GroupCreationRequest

grouprouter = APIRouter(prefix="/api/group")

# DEBUG
@grouprouter.get("/")
def getAllGroups():
    return 0

@grouprouter.get("/{groupid}")
def getGroupByID(groupid: int) -> Group:
    return 0

@grouprouter.post("/")
def createGroup(group: GroupCreationRequest) -> Group:
    return 0

@grouprouter.put("/{groupid}")
def updateGroup(groupid: int, group: GroupCreationRequest) -> Group:
    return 0

@grouprouter.delete("/{groupid}")
def deleteGroup(groupid: int) -> str:
    return 0


@grouprouter.post("/{groupid}/")
def addUserToGroup(groupid: int, userId: int) -> str:  # accepted invite and admin accepts user
    return 0

@grouprouter.post("/{groupid}/invite/{userId}")
def inviteUserToGroup(groupsid: int, userId: int) -> str:  # send invite
    return 0

@grouprouter.delete("/{groupid}/{userid}")
def deleteUserFromGroup(groupid : int, userid: int) -> str:
    return 0