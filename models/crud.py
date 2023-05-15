from sqlalchemy.orm import Session
from models.models import *
from models.schemas import *


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id, User.status == False).first()


# 新建用户
def db_create_user(db: Session, user: UserCreate):
    roles = db.query(Role).filter(Role.name == user.role).first()
    db_user = User(**user.dict())
    db_user.role = roles.id
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username, User.status == False).first()


def get_role_name(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()
