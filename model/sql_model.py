from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime, Integer
import datetime

def get_current_time():
    return datetime.datetime.now()

BASE = declarative_base()

class Todo(BASE):
    __tablename__ = 'to_do'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=get_current_time())
    updated_at = Column(DateTime, default=get_current_time(), onupdate=get_current_time())

    def __repr__(self, todo):
        self.todo = todo