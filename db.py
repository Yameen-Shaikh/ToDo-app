from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from typing import Annotated
from fastapi import Depends

engine = create_engine('postgresql://postgres:0000@localhost:5432/postgres', echo=False)

SessionLocal = sessionmaker(bind=engine)

