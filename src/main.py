from fastapi import FastAPI, HTTPException, Request
from .models.User import User
from .database import DB
from typing import List
from sqlmodel import select
from .routes.User import userrouter
from .routes.Transaction import transactionRouter
from .routes.Group import grouprouter
from .models.models import LoginRequest, LoginResponse
import datetime

app = FastAPI()

app.include_router(userrouter)
app.include_router(transactionRouter)
app.include_router(grouprouter)

@app.post("/api/login")
def login(data: LoginRequest) -> LoginResponse:
    if data.username == data.password:
        return LoginResponse(token="abc", expiration=datetime.datetime.now())
    raise HTTPException(
        status_code=401,
        detail="mock"
    )

@app.post("/api/logout")
def logout() -> str:
    return 0

@app.get("/api/test")
def test_token(r: Request) -> str:
    h = r.headers.get("Authorization")
    if not h or not h.startswith("Bearer ") or not h.split("Bearer ")[1]:
        raise HTTPException(
            status_code=401,
            detail="mock"
        )
    return "ok"