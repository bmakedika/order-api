from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Header, HTTPException, Depends
from fastapi.security import HTTPBearer
from app.core.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES


security = HTTPBearer()


def create_access_token(username: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {
        'sub': username,
        'role': role,
        'exp': expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid or expired token')


def require_admin(credentials = Depends(security)):
    token = credentials.credentials
    return decode_token(token)


def require_user(credentials = Depends(security)):
    token = credentials.credentials
    return decode_token(token)