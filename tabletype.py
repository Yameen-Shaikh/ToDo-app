from pydantic import BaseModel


class PydTask(BaseModel):
    title:str 
    details:str
    
    
