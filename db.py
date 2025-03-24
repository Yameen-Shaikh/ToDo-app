from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:0000@localhost:5432/postgres', echo=False)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()