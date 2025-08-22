from database import Base,session_local
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="Users"
    id=Column(Integer,autoincrement=True,primary_key=True,index=True)
    name=Column(String,index=True)
    email=Column(String)
    tasks=relationship("Task")
    
class Task(Base):
    __tablename__="Tasks"
    id=Column(Integer,index=True,autoincrement=True,primary_key=True)
    title=Column(String)
    description=Column(String)
    status=Column(String,default="todo")
    owner_id=Column(Integer,ForeignKey("Users.id"),index=True,)
    # owner=relationship("User",back_populates="tasks")
