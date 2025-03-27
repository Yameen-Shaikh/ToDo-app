from pydantic import BaseModel
from datetime import date
from models import TaskPriority
from enums import TaskPriority


class PydUser(BaseModel):
    username: str
    password: str

class PydTask(BaseModel):
    title: str 
    details: str
    date: date
    completed: bool = False  # Default value
    priority: TaskPriority = TaskPriority.MEDIUM  # Default medium priority
    user: PydUser 
    
    class Config:
        orm_mode = True
        use_enum_values = True #this will converts enums to strings in JSON
    
class updatedTask(PydTask):
    title: str = None
    details: str = None

class Token(BaseModel):
    access_token: str
    token_type: str