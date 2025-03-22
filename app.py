from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user,pwd_context
from db import SessionLocal
from models import Task
from tabletype import PydTask, Token
from models import User
from fastapi.security import OAuth2PasswordRequestForm
from tabletype import PydUser
from datetime import timedelta
from sqlalchemy.orm import Session

app = FastAPI()

# ?
# router = APIRouter(
#     prefix='/auth',
#     tags=['auth']
# )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

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

# fetch users(NOT WORKING)
@app.get("/users")
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401)
    return user
# #---------------------------------------- CRUD operations ----------------------------------------
# @app.post("/create-task")
# async def create_task(task: PydTask):
#     db = Session()
#     todo = Task(title=task.title, details=task.details)
#     db.add(todo)
#     db.commit()
#     return {"Task added successfully!🥳"}

# @app.get("/get-tasks")
# async def get_tasks():
#     db = Session()
#     query = db.query(Task)
#     return query.all()

# @app.get("/task-details/{id}")
# async def read_task(id: int):
#     db = Session()
#     task = db.query(Task).filter(Task.id == id).first()
#     if Task.id != id:
#         raise HTTPException(status_code=400, detail="Task with {id} not found!")
#     return task

# @app.put("/update-task/{id}")
# async def update_task(id: int, task: PydTask):
#     db = Session()
#     todo = db.query(Task).filter(Task.id == id).first()
#     todo.title = task.title
#     todo.details = task.details
#     db.commit()
#     return {"message":"Task updated", "task":todo}
        
# @app.delete("/delete-task/{id}")
# async def delete_task(id: int):
#     db = Session()
#     task = db.query(Task).filter(Task.id == id).first()
#     db.delete(task)
#     db.commit()
#     return {"message":"Task deleted", "task":task}
