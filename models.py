import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase
from db import engine


class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    details = Column(String(50))
    date_time = Column(DateTime, default=datetime.datetime.now)
    completed = Column(Boolean, default=False)
    priority = Column(Integer, default=1)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    hashed_password = Column(String(100))

Base.metadata.create_all(engine)