from pydantic import BaseModel, Field,EmailStr
from typing import Annotated
from enum import Enum

class Userbase(BaseModel):
    name:Annotated[str, Field(min_length=3,max_length=60,description="First name,Last name")]
    email:EmailStr

class user(Userbase):
    id:int
    class Config:
        from_attributes=True 

class Status(Enum):
    todo = "todo"
    in_progress = "in progress"
    done = "done"
 
class Taskbase(BaseModel):
    title:Annotated[str,Field(min_length=2,max_length=100)]
    description:Annotated[str,Field(min_length=2,max_length=255)]
    owner_id:int
    status:Status = "todo"
        
class task(Taskbase):
    id:int
    class Config:
        from_attributes=True
        
class usercreate(Userbase):
    pass
      
class taskcreate(Taskbase):
    pass
    
