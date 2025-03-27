import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Enum, Text
from sqlalchemy.orm import DeclarativeBase, relationship
from db import engine
from enums import TaskPriority

class Base(DeclarativeBase):
    pass

    
class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    details = Column(Text)
    priority = Column(Enum(TaskPriority), default='medium')
    date_time = Column(Date, default=datetime.datetime.today)
    due_date = Column(Date, nullable=True) 
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("user.id"))   

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    hashed_password = Column(String(100))
    tasks = relationship(Task)

Base.metadata.create_all(engine)