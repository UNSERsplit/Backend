from fastapi import FastAPI
from .models import User
from .database import DB
from typing import List
from sqlmodel import select

app = FastAPI()

@app.get("/api/")
def test(db: DB) -> List[User]:
    return db.exec(select(User)).all()

@app.post("/api/test")
def test_post(user: User, db: DB) -> str:
    db.add(user)
    db.commit()
    db.refresh(user)
    return "ok"