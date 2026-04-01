from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import create_access_token, require_user
from app.schemas.auth import TokenResponse
from app.schemas.user import UserRegister, UserLogin, UserResponse
from app.services import user_service
from app.repos.user_repo import get_by_email


router = APIRouter()

# register
@router.post('/auth/register', response_model=UserResponse)
def register(body: UserRegister, db: Session = Depends(get_db)):
    user = user_service.register_user(db, username=body.username, email=body.email, password=body.password)
    return user

# create_access_token in login endpoint
@router.post('/auth/login', response_model=TokenResponse)
def login(body: UserLogin, db: Session = Depends(get_db)):
    user = user_service.login_user(db, email=body.email, password=body.password)

    token = create_access_token(username=user.email, role=user.role)
    return {
        'access_token': token,
        'token_type': 'bearer'
    }

# get current user info
@router.get('/auth/me', response_model=UserResponse)
def me(payload = Depends(require_user), db: Session = Depends(get_db)):
    user = get_by_email(db, email=payload['sub'])
    return user