from sqlalchemy.orm import Session
from uuid import UUID
from app.models.user import UserModel


# CREATE

def create(db: Session, data: dict) -> UserModel:
    user = UserModel(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# READ

def get_by_id(db: Session, id: UUID) -> UserModel:
    return db.query(UserModel).filter(UserModel.id == id).first()

def get_by_email(db: Session, email: str) -> UserModel:
    return db.query(UserModel).filter(UserModel.email == email).first()
