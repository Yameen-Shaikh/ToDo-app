from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user,pwd_context
from db import SessionLocal
from tabletype import PydTask, Token, updatedTask
from models import Task, User
from fastapi.security import OAuth2PasswordRequestForm
from tabletype import PydUser
from datetime import timedelta
from sqlalchemy.orm import Session

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
        hashed_password = pwd_context.hash(create_user.password)
    )
    db.add(create_user_model)
    db.commit()
    return {"message":"User created successfully!🤗"}

# generating token
@app.post("/token", response_model=Token)
async def login_for_access(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user =  authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(user.id, user.username, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

# fetch user
@app.get("/user")
def get_current_user(current_user: dict = Depends(get_current_user)):
    return current_user

# #---------------------------------------- CRUD operations ----------------------------------------
@app.post("/create-task")
async def create_task(task: PydTask, db: Session = Depends(get_db)):
    new_task = Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"Task added successfully!🥳", new_task}

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
