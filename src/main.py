from fastapi import Depends, FastAPI, HTTPException, Request
from .models.User import User
from .database import DB
from typing import List
from sqlmodel import select
from .routes.User import userrouter
from .routes.Transaction import transactionRouter
from .routes.Group import grouprouter
from .routes.Friends import friendsRouter
from .models.models import LoginRequest, LoginResponse
from .auth import authrouter, get_current_user
import firebase_admin

default_app = firebase_admin.initialize_app()

app = FastAPI(redirect_slashes=False)

app.include_router(userrouter)
app.include_router(transactionRouter)
app.include_router(grouprouter)
app.include_router(authrouter)
app.include_router(friendsRouter)

@app.get("/api/test")
def test_token(user: User = Depends(get_current_user)) -> str:
    return "ok"