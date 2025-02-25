from fastapi import APIRouter
from ..database import DB
from typing import List
from sqlmodel import select
from ..models.Group import Group

grouprouter = APIRouter(prefix="/api/group")

@grouprouter.get("/")
def getAllGroups():
    return 0

@grouprouter.get("/{groupid}")
def getGroupByID(groupid: int):
    return 0

@grouprouter.post("/")
def createGroup(group: Group):
    return 0

@grouprouter.put("/{groupid}")
def updateGroup(groupid: int):
    return 0


@grouprouter.delete("/{groupid}")
def deleteGroup(groupid: int):
    return 0

@grouprouter.post("/{groupid}/")
def addUserToGroup(groupid: int):  # accepted invite and admin accepts user
    return 0

@grouprouter.post("/{groupid}/invite")
def inviteUserToGroup(groupid: int):  # send invite
    return 0

@grouprouter.delete("/{groupid}/{userid}")
def deleteUserFromGroup(groupid : int, userid: int):
    return 0