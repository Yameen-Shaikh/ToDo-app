from pydantic import BaseModel


class PydTask(BaseModel):
    title:str 
    details:str
    
class updatedTask(PydTask):
    title: str = None
    details: str = None
    
class PydUser(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str