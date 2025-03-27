from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user,pwd_context
from db import SessionLocal
from tabletype import PydTask, Token
from models import Task, User
from fastapi.security import OAuth2PasswordRequestForm
from tabletype import PydUser
from datetime import timedelta
from sqlalchemy.orm import Session
from datetime import datetime

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

#---------------------------------------- User ----------------------------------------
@app.post("/signin", status_code=201)
async def create_user(create_user: PydUser, db: db_dependency):
    create_user_model=User(
        username = create_user.username, 
        hashed_password = pwd_context.hash(create_user.password))
    db.add(create_user_model)
    db.commit()
    return {"message":"User created successfully!🤗"}

# generating token for login
@app.post("/login", response_model=Token)
async def login_for_access(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user =  authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(user.id, user.username, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

# fetch user
@app.get("/user")
def get_user(current_user: dict = Depends(get_current_user)):
    return current_user

#---------------------------------------- CRUD operations ----------------------------------------
@app.post("/tasks", status_code=201)
async def create_task(
    task_data: PydTask,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Ensure this returns User model
):
    db_task = Task(
        **task_data.model_dump(),
        user_id=current_user.id  # Auto-inject user ID
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/get-tasks")
async def get_tasks(db: Session = Depends(get_db)):
    query = db.query(Task)
    return query.all()

@app.get("/task-details/{id}")
async def read_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if task is None:
        raise HTTPException(status_code=400, detail=f"Task with {id} not found!")
    return task

@app.put("/update-task/{id}")
async def update_task(id: int, task: PydTask, db: Session = Depends(get_db)):
    todo = db.query(Task).filter(Task.id == id).first()
    todo.title = task.title
    todo.details = task.details
    db.commit()
    return {"message":"Task updated", "task":task}

        
@app.delete("/delete-task/{id}")
async def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    db.delete(task)
    db.commit()
    return {"message":"Task deleted", "task":task}

@app.get("/get-tasks/{date}")
async def get_task_bydate(db: Session = Depends(get_db)):
    task = db.query(Task).order_by(Task.date_time).all()
    return task

#filter by id/title/date
@app.get("/get-task/{search}")
async def search_task(id: int = None, title: str = None, date: datetime = None, db: Session = Depends(get_db)):
    if id:
        task = db.query(Task).filter(Task.id == id).first()
    elif title:
        task = db.query(Task).filter(Task.title == title).first()
    elif date:
        task = db.query(Task).filter(Task.date_time == date).first()
    else:
        raise HTTPException(status_code=404, detail=f"task not found with {search_task}")
    
    return task
