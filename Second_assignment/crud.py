from sqlalchemy.orm import Session
import models

def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def create_user(db: Session, user_id: str):
    db_user = models.User(user_id=user_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_access(db: Session, access_id: str):
    return db.query(models.Access).filter(models.Access.access_id == access_id).first()

def create_access(db: Session, access_id: str, user_id: str, channel_id: str):
    db_access = models.Access(access_id=access_id, user_id=user_id, channel_id=channel_id)
    db.add(db_access)
    db.commit()
    db.refresh(db_access)
    return db_access
