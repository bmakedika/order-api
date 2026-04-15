from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import create_access_token, create_refresh_token, decode_token
from app.core.refresh_store import store_refresh_token, get_subject_for_refresh_token, revoke_refresh_token
from app.schemas.auth import TokenResponse, RefreshRequest, LogoutRequest
from app.schemas.user import UserRegister, UserLogin, UserResponse
from app.services import user_service
from app.repos.user_repo import get_by_email


router = APIRouter()

# register
@router.post('/auth/register', response_model=UserResponse)
def register(body: UserRegister, db: Session = Depends(get_db)):
    return user_service.register_user(db, username=body.username, email=body.email, password=body.password)

# create_access_token in login endpoint
@router.post('/auth/login', response_model=TokenResponse)
def login(body: UserLogin, db: Session = Depends(get_db)):
    user = user_service.login_user(db, email=body.email, password=body.password)

    access_token = create_access_token(subject=user.email, role=user.role)
    refresh_token = create_refresh_token(subject=user.email, role=user.role)
    store_refresh_token(refresh_token, subject=user.email)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }

# get current user info
@router.post('/auth/refresh', response_model=TokenResponse)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    # 1. JWT must be valid and must be a refresh token
    payload = decode_token(body.refresh_token)
    if payload.get('type') != 'refresh':
        raise HTTPException(status_code=401, detail='Invalid refresh token')
    # 2. JWt must exist in Redis (not revoked)
    subject = get_subject_for_refresh_token(body.refresh_token)
    if not subject:
        raise HTTPException(status_code=401, detail='Invalid refresh token')
    # 3. Ensure user still exists
    user = get_by_email(db, email=subject)
    if not user:
        # revoke silentely to clean redis
        revoke_refresh_token(body.refresh_token)
        raise HTTPException(status_code=401, detail='Invalid refresh token')
    # 4. Rotation: revoke old, issue new refresh, store new
    revoke_refresh_token(body.refresh_token)

    new_access = create_access_token(subject=user.email, role=user.role)
    new_refresh = create_refresh_token(subject=user.email, role=user.role)
    store_refresh_token(new_refresh, subject=user.email)
    return {
        'access_token': new_access,
        'refresh_token': new_refresh,
        'token_type': 'bearer'
    }

@router.post('/auth/logout')
def logout(body: LogoutRequest):
    revoke_refresh_token(body.refresh_token)
    return {'detail': 'Logged out successfully'}