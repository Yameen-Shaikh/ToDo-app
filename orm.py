import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine('postgresql://postgres:0000@localhost:5432/postgres', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    details = Column(String(50))
    date_time = Column(DateTime, default=datetime.datetime.now)
    status = Column(Boolean, default=False)
    priority = Column(Integer, default=1)
    
add_task1 = Task(title = 'Completed REST API', details = 'Watch videos')
add_task2 = Task(title = 'Completed Python', details = 'Practise core concepts')
add_task3 = Task(title = 'Completed OOPs', details = 'Take hand on experience')
session.add_all([add_task1, add_task2, add_task3])
session.commit()
    
# Base.metadata.create_all(engine)