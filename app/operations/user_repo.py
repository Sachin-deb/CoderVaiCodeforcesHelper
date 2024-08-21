import sys
sys.path.append('./')
from sqlalchemy.orm import Session
from app.model.user import User 
from app.database.connection import db_session
from app.schemas.user_schema import *

def create_user(user_data: UserCreate, password_hash: str):
    user = User(
        handle=user_data.handle,
        username=user_data.username,
        password_hash=password_hash,
        email=user_data.email,
        vjudge_handle=user_data.vjudge_handle
    )
    db_session.add(user)
    db_session.commit()
    return user

def get_user_by_handle(handle: str):
    return db_session.query(User).filter(User.handle == handle).first()

def get_user_by_email(email: str):
    return db_session.query(User).filter(User.email == email).first()

def get_user_by_username(username: str):
    return db_session.query(User).filter(User.username == username).first()

def get_all_users():
    return db_session.query(User).all()

def update_user(handle: str, **kwargs):
    user = get_user_by_handle(handle)
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value)
        db_session.commit()
    return user

def delete_user(handle: str):
    user = get_user_by_handle(handle)
    if user:
        db_session.delete(user)
        db_session.commit()
    return user is not None
