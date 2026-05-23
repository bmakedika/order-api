from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from app.repos.user_repo import create, get_by_email

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def register_user(db: AsyncSession, username: str, email: str, password: str):
    existing_user = await get_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=409, detail='Conflict')

    hashed_password = pwd_context.hash(password)
    return await create(db, {
        'username':        username,
        'email':           email,
        'hashed_password': hashed_password,
    })


async def login_user(db: AsyncSession, email: str, password: str):
    user = await get_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')

    if not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Unauthorized')

    return user