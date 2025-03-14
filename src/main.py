from fastapi import FastAPI
from .models.User import User
from .database import DB
from typing import List
from sqlmodel import select
from .routes.User import userrouter
from .routes.Transaction import transactionRouter
from .routes.Group import grouprouter
from .models.models import LoginRequest, LoginResponse
from auth import authrouter

app = FastAPI()

app.include_router(userrouter)
app.include_router(transactionRouter)
app.include_router(grouprouter)
app.include_router(authrouter)

@app.post("/api/login")
def login(data: LoginRequest) -> LoginResponse:
    return 0

@app.post("/api/logout")
def logout() -> str:
    return 0