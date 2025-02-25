from fastapi import FastAPI
from .models.User import User
from .database import DB
from typing import List
from sqlmodel import select
from .routes.User import userrouter
from .routes.Transaction import transactionRouter
from .routes.Group import grouprouter

app = FastAPI()

app.include_router(userrouter)
app.include_router(transactionRouter)
app.include_router(grouprouter)

@app.post("api/login")
def login():
    return 0

@app.post("api/logout")
def logout():
    return 0