from fastapi import FastAPI
from orm import Task, session
from tabletype import PydTask

app = FastAPI()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/createTask")
async def insert_task(task: PydTask):
    todo = Task(title=task.title, details=task.details)
    session.add(todo)
    session.commit()
    return {"Task added successfully!🥳"}

@app.get("/getTasks")
async def get_all_task():
    query = session.query(Task)
    return query.all()

# @app.get("/getTaskDetails/{id}")
# async def get_task_details(id:int, db:session = Depends(get_db)):
#     tesk = db.query(Task).filter(Task.id == id).first()
#     # query = session.query(Task).filter(Task.id == id)
#     # task = query.first()
#     return query.all()
    
