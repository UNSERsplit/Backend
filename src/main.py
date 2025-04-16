from fastapi import Depends, FastAPI, HTTPException, Request
from .models.User import User
from .database import DB
from typing import List
from sqlmodel import select
from .routes.User import userrouter
from .routes.Transaction import transactionRouter
from .routes.Group import grouprouter
from .models.models import LoginRequest, LoginResponse
from .auth import authrouter, get_current_user
import firebase_admin
from firebase_admin import messaging

default_app = firebase_admin.initialize_app()

app = FastAPI(redirect_slashes=False)

app.include_router(userrouter)
app.include_router(transactionRouter)
app.include_router(grouprouter)
app.include_router(authrouter)

@app.get("/api/test")
def test_token(user: User = Depends(get_current_user)) -> str:
    return "ok"

@app.post("/api/message")
def send_message(device_token: str, title: str, text: str) -> str:
    message = messaging.Message(
        data={
            'title':title,
            'text':text
        },
        token=device_token
    )

    return messaging.send(message)