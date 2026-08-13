from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

password_hash = PasswordHash.recommended()

SECRET_KEY = os.getenv("TASK_API_SECRET_KEY")
ALGORITHM = "HS256"


def hash_password(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None=None):
    to_encode = data.copy()

    if expires_delta:
        expire=datetime.now(timezone.utc) + expires_delta
    else:
        expire= datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp":expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)