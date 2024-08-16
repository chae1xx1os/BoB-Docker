from sqlalchemy.orm import Session
import models
import schema

def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def create_user(db: Session, user: schema.UserCreate):
    db_user = models.User(user_id=user.user_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

def create_access(db: Session, access_id: str, user_id: str, channel_id: str):
    db_access = models.Access(access_id=access_id, user_id=user_id, channel_id=channel_id)
    db.add(db_access)
    db.commit()
    db.refresh(db_access)
    return db_access

def write_ioc(db: Session, ioc_data: schema.IoC_Data):
    db_ioc = models.IoC(
        id=ioc_data.id,
        indicator=ioc_data.ioc_item,
        ioc_type=ioc_data.ioc_type,
        description=ioc_data.description,
        last_seen=ioc_data.last_seen
    )
    db.add(db_ioc)
    db.commit()
    db.refresh(db_ioc)
    return db_ioc

def get_ioc(db: Session):
    return db.query(models.IoC).all()
