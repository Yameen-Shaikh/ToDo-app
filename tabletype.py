from pydantic import BaseModel


class PydTask(BaseModel):
    title:str 
    details:str
    
class PydUser(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str