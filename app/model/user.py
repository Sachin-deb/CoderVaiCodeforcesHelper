from sqlalchemy import Column, Integer, String, DateTime, func
from app.model import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    handle = Column(String(50), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    vjudge_handle = Column(String(50), unique=True, nullable=True)

    is_active = Column(Integer, default=1)  # Flag to indicate if the user is active
    is_admin = Column(Integer, default=0)  # Flag to indicate if the user has admin rights

    def __repr__(self):
        return f"<User(handle={self.handle}, username={self.username}, email={self.email})>"