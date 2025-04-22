from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional

import firebase_admin
from firebase_admin import messaging

class _PublicUserData(BaseModel):
    firstname: str
    lastname: str
    iban: Optional[str] = None

class PublicUserData(_PublicUserData):
    userid: Optional[int] = Field(default=None, primary_key=True)

class PrivateUserData(BaseModel):
    email: EmailStr = Field(unique=True)
    password: str

class UserCreateRequest(_PublicUserData, PrivateUserData):
    pass

class Action:
    def __init__(self):
        self.data = {}

class OpenGroupAction(Action):
    def __init__(self, groupId: int):
        super().__init__()

        self.data["action"] = "showGroup"
        self.data["groupId"] = str(groupId)

class User(SQLModel, UserCreateRequest, PublicUserData, table=True):
    fcm_device_token: Optional[str] = Field(default=None)

    def send_message(self, title: str, text: str, action: Action = None) -> str:
        if not self.fcm_device_token:
            print(f"fcm_device_token must be set in order to send messages {self.userid}")
            return
        
        data = {
                'title':title,
                'text':text
            }
    
        if action:
            data.update(action.data)

        message = messaging.Message(
            data=data,
            token=self.fcm_device_token
        )

        return messaging.send(message)