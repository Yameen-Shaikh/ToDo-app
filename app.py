from fastapi import FastAPI
from models import Task, session
from tabletype import PydTask
from models import Session

app = FastAPI()

#-----------------------------------CRUD operations-----------------------------------
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
    return task
    
@app.delete("/delete-task/{id}")
async def delete_task(id: int):
    db = Session()
    task = db.query(Task).filter(Task.id == id).first()
    db.delete(task)
    db.commit()
    return {"message":"Task deleted", "task":task}
            