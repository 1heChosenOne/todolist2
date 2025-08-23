from fastapi import FastAPI,Depends,HTTPException
from database import Base,session_local,engine
from columns import User,Task
from pydantic_schemas import user,usercreate,taskcreate,task,Status
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import func

 
app=FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()
        
def task_validator(task_id:int,db:Session):
    maxid=db.query(func.max(Task.id)).scalar()
    if task_id is None:
        raise HTTPException(status_code=404,detail=f"no task id provided")
    if task_id > maxid or task_id <= 0:
        raise HTTPException(status_code=404,detail=f"Task with id {task_id} not found")

def user_validator(user_id:int,db:Session):
    maxid=db.query(func.max(User.id)).scalar()
    if user_id is None:
        raise HTTPException(status_code=404,detail=f"no task id provided")
    if user_id > maxid or user_id == 0:
        raise HTTPException(status_code=404,detail=f"User with id {user_id} not found")


@app.get("/Users")
async def allusers(db:Annotated[Session,Depends(get_db)]):
    return db.query(User).all()

@app.get("/Tasks")
async def alltasks(db:Annotated[Session,Depends(get_db)]):
    return db.query(Task).all()

@app.get("/Users/{user_id}")
async def useridinfo(user_id:int,db:Annotated[Session,Depends(get_db)]):
    maxid=db.query(func.max(User.id)).scalar()
    if user_id > maxid or user_id == 0:
        raise HTTPException(status_code=404,detail=f"User with id {user_id} not found")    
    return db.query(User).filter(User.id==user_id).first()

@app.get("/Users/{user_id}/tasks")
async def getusertask(user_id:int,db:Annotated[Session,Depends(get_db)]):
    maxid=db.query(func.max(User.id)).scalar()
    if user_id > maxid or user_id == 0:
        raise HTTPException(status_code=404,detail=f"User with id {user_id} not found")
    alltasks=db.query(Task).filter(user_id== Task.owner_id).all()
    return alltasks

@app.get("/Tasks/{task_id}")
async def useridinfo(task_id:int,db:Annotated[Session,Depends(get_db)]):
    maxid=db.query(func.max(Task.id)).scalar()
    if task_id > maxid or task_id == 0:
        raise HTTPException(status_code=404,detail=f"Task with id {task_id} not found")    
    return db.query(Task).filter(Task.id==task_id).first()
    
    

@app.post("/Users/add",response_model=user)
async def users_add(user:usercreate,db:Annotated[Session,Depends(get_db)]):
    adduser=User(name=user.name,email=user.email)
    db.add(adduser)
    db.commit()
    db.refresh(adduser)
    return adduser

@app.post("/Users/Tasks/add")
async def addtasks(task1:taskcreate,db:Annotated[Session,Depends(get_db)]):
    userid=db.query(User).filter(User.id == task1.owner_id).first()
    if userid is None:
        raise HTTPException(status_code=404,detail="owner not found")
    addtask=Task(title=task1.title,description=task1.description,owner_id=userid.id)
    db.add(addtask)
    db.commit()
    db.refresh(addtask)
    return addtask

@app.patch("/Tasks/{task_id}")
async def updatestatus(task_id:int,userinfo:Annotated[Status,"only 3 values: todo, in progress, done"],db:Annotated[Session,Depends(get_db)]):
    task_validator(task_id,db)
    updatabletask=db.query(Task).filter(Task.id == task_id).first()
    updatabletask.status=userinfo.value
    db.commit()
    db.refresh(updatabletask)
    return updatabletask,userinfo

@app.delete("/Tasks/{task_id}")
async def deletetask(task_id:int,db:Annotated[Session,Depends(get_db)]):
    user_validator(task_id,db)
    deletabletask=db.query(Task).filter(Task.id==task_id).first()
    db.delete(deletabletask)
    db.commit()
    return {"message":f"Task with id {task_id} deleted succesfully"}
    
    