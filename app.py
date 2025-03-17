from fastapi import FastAPI, HTTPException
from models import Task
from tabletype import PydTask
from models import Session


app = FastAPI()

#---------------------------------------- CRUD operations ----------------------------------------
@app.post("/create-task")
async def create_task(task: PydTask):
    db = Session()
    todo = Task(title=task.title, details=task.details)
    db.add(todo)
    db.commit()
    return {"Task added successfully!🥳"}

@app.get("/get-tasks")
async def get_tasks():
    db = Session()
    query = db.query(Task)
    return query.all()

@app.get("/task-details/{id}")
async def read_task(id: int):
    db = Session()
    task = db.query(Task).filter(Task.id == id).first()
    if Task.id != id:
        raise HTTPException(status_code=400, detail="Task with {id} not found!")
    return task

@app.put("/update-task/{id}")
async def update_task(id: int, task: PydTask):
    db = Session()
    todo = db.query(Task).filter(Task.id == id).first()
    todo.title = task.title
    todo.details = task.details
    db.commit()
    return {"message":"Task updated", "task":todo}
        
@app.delete("/delete-task/{id}")
async def delete_task(id: int):
    db = Session()
    task = db.query(Task).filter(Task.id == id).first()
    db.delete(task)
    db.commit()
    return {"message":"Task deleted", "task":task}
            
