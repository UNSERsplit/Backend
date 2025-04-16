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

class User(SQLModel, UserCreateRequest, PublicUserData, table=True):
    fcm_device_token: Optional[str] = Field(default=None)

    def send_message(self, title: str, text: str) -> str:
        if not self.fcm_device_token:
            raise ValueError("fcm_device_token must be set in order to send messages")
        message = messaging.Message(
            data={
                'title':title,
                'text':text
            },
            token=self.fcm_device_token
        )

        return messaging.send(message)