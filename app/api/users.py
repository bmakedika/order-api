from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import require_user
from app.repos.user_repo import get_by_email
from app.schemas.user import UserResponse

router = APIRouter()

@router.get('/users/me', response_model = UserResponse)
def get_me(payload=Depends(require_user), db: Session = Depends(get_db)):
    user = get_by_email(db, email=payload['sub'])
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user