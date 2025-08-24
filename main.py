from fastapi import FastAPI,Depends,HTTPException

from database import engine
from pydantic_schemas import user,usercreate,taskcreate,task,Status
from typing import Annotated
from sqlalchemy import text

app=FastAPI()

def get_conn(): 
    conn=engine.connect()
    try:
        yield conn
    finally:
        conn.close()
        
def get_begin():
    with engine.begin() as begin:
        yield begin

def task_max_id():
    with engine.connect() as conn:
        maxid=conn.execute(text("SELECT MAX(id) FROM tasks")).fetchone()
    return maxid[0]
 
def user_max_id():
    with engine.connect() as conn:
        maxid=conn.execute(text("SELECT MAX(id) FROM users")).fetchone()
        return maxid[0]
        
def task_validator(task_id:int):
    maxid=task_max_id()
    if task_id is None:
        raise HTTPException(status_code=404,detail=f"no task id provided")
    if task_id > maxid or task_id <= 0:
        raise HTTPException(status_code=404,detail=f"Task with id {task_id} not found")
    with engine.connect() as conn:
        result=conn.execute(text("SELECT * FROM tasks WHERE id=:task_id"),{"task_id":task_id}).fetchone()
        if result is None:
            raise HTTPException(status_code=404,detail=f"no user with id {task_id}")

def user_validator(user_id:int): 
    maxid=user_max_id()
    if user_id is None:
        raise HTTPException(status_code=404,detail=f"no task id provided")
    if user_id > maxid or user_id <= 0:
        raise HTTPException(status_code=404,detail=f"User with id {user_id} not found")
    with engine.connect() as conn:
        result=conn.execute(text("SELECT * FROM users WHERE id=:id"),{"id":user_id}).fetchone()
        if result is None:
            raise HTTPException(status_code=404,detail=f"no user with id {user_id}")
    
def owner_id_validator(owner_id):
    with engine.connect() as conn:
        real_owner_id=conn.execute(text("SELECT id FROM users WHERE id=:owner_id"),{"owner_id":owner_id}).fetchone()
        if real_owner_id is None:
            raise HTTPException(status_code=404,detail=f"Owner with id {owner_id} not found")
    
    
@app.get("/Users")
async def get_all_users(conn=Depends(get_conn)):
    result=conn.execute(text("SELECT * FROM users")).fetchall()
    return (dict(row._mapping) for row in result)

@app.get("/Tasks")
async def get_all_tasks(conn=Depends(get_conn)):
    result=conn.execute(text("SELECT * FROM tasks")).fetchall()
    return (dict(row._mapping) for row in result)

@app.get("/Users/{user_id}")
async def get_user(user_id:int,conn=Depends(get_conn)):
    user_validator(user_id)
    result=conn.execute(text("SELECT * FROM users WHERE id=:user_id"),{"user_id":user_id}).fetchone()
    return (dict(result._mapping))

@app.get("/Users/{user_id}/tasks")
async def get_user_task(user_id:int,conn=Depends(get_conn)):
    user_validator(user_id)
    result=conn.execute(text("SELECT * FROM tasks WHERE owner_id=:user_id"),{"user_id":user_id}).fetchall()
    return (dict(row._mapping)for row in result)

@app.get("/Tasks/{task_id}")
async def get_task(task_id:int,conn=Depends(get_conn)):
    task_validator(task_id)
    result=conn.execute(text("SELECT * FROM tasks WHERE id=:task_id"),{"task_id":task_id}).fetchone()
    return dict(result._mapping)

@app.post("/Users/add")
async def add_user(user:usercreate,conn=Depends(get_conn)):
    result=conn.execute(text("INSERT INTO users (name,email) VALUES (:name,:email)"),{"name":user.name,"email":user.email})
    conn.commit()
    new_id=result.lastrowid
    new_user=conn.execute(text("SELECT * FROM users WHERE id=:id"),{"id":new_id}).fetchone()
    return dict(new_user._mapping)

@app.post("/Users/Tasks/add")
async def add_tasks(task:taskcreate,conn=Depends(get_conn)):
    owner_id_validator(task.owner_id) 
    result=conn.execute(text("INSERT INTO tasks (title,description,owner_id) VALUES(:title, :description, :owner_id)"),{"title":task.title,
                                                                                                                        "description":task.description,
                                                                                                                        "owner_id":task.owner_id})
    conn.commit()
    new_id=result.lastrowid
    new_task=conn.execute(text("SELECT * FROM tasks WHERE id=:new_id"),{"new_id":new_id}).fetchone()
    return dict(new_task._mapping)  

@app.patch("/Tasks/{task_id}")
async def update_status(task_id:int,user_info:Status,conn=Depends(get_conn)):
    task_validator(task_id)
    conn.execute(text("UPDATE tasks SET status =:user_info WHERE id=:task_id"),{"user_info":user_info.value,"task_id":task_id})
    conn.commit()
    result=conn.execute(text("SELECT * FROM tasks WHERE id=:id"),{"id":task_id}).fetchone()
    return dict(result._mapping) 

@app.delete("/Tasks/{task_id}")
async def delete_task(task_id:int,conn=Depends(get_conn)):
    task_validator(task_id)
    result=conn.execute(text("SELECT * FROM tasks WHERE id=:id"),{"id":task_id}).fetchone()
    deletable_user=dict(result._mapping)
    conn.execute(text("DELETE FROM tasks WHERE id=:id"),{"id":task_id})
    conn.commit()
    return {"message":f"task with id {task_id} and attributes {deletable_user} deleted"}

