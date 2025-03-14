
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from .database import DB

from datetime import timedelta, datetime
from .models.User import User
import jwt
from passlib.context import CryptContext
from typing import Union, Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str

authrouter = APIRouter(prefix="/api/auth")

SECRET_KEY = "abcdefghijklmnopqrstuvwxyz"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43800  # 1 Month

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def verify_password(plain_passwd, hashed_password):
    return pwd_context.verify(plain_passwd, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: DB, email: str, password: str) -> Union[bool, User]:
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: DB, token: str = Depends(oauth_2_scheme)) -> User:
    credential_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credential_exceptions
        token_data = TokenData(email=email)
    except Exception:
        raise credential_exceptions
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credential_exceptions

    return user


@authrouter.post("/token", response_model=Token)
async def login_for_access_token(db: DB, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="Bearer")




# https://www.youtube.com/watch?v=5GxQ1rLTwaU
