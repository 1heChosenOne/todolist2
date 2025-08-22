# from fastapi import FastAPI , HTTPException
# from typing import Optional,List
# from pydantic import BaseModel
# app = FastAPI()
# class human(BaseModel):
#     id:int
#     name:str
#     age:int

# class item(BaseModel):
#     id:int
#     title:str
#     author:human

# class item_create(BaseModel):
#     title:str
#     author_id:int
    
# humans=[
#     {"id":1,"name":"Skebob","age":52},
#     {"id":2,"name":"Roblox_Egor","age":25}   
#         ]
# posts=[{"id":1,"title":"title 1","author":humans[0]},
#    {"id":2,"title":"title 2","author":humans[1]}]

# @app.get("/")
# async def home() -> dict[str,str]:
#     return {"data":"message"}


# @app.post("/items/add")
# async def item_add(item1:item_create) -> item:
#     author = next((human1 for human1 in humans if human1["id"] ==item1.author_id),None)
#     if not author:
#         raise HTTPException(status_code=404,detail="author not found")
#     id1=len(posts)+1
#     post={"id":id1,"title":item1.title,"author":human(**author)}
#     posts.append(post)
#     return item(**post)
    
    

# # @app.get("/items")
# # async def items():
# #     return posts

# @app.get("/items")
# async def items() -> List[item]:
#     return [item(**post) for post in posts]
    

# @app.get("/items/{id}")
# async def items(id:int) -> item:
#     for i in posts:
#         if i["id"] == id:
#             return item(**i)
#     raise HTTPException(status_code=404,detail="Post not found,okak")

# @app.get("/search")
# async def search(item_id: Optional[int]=None) -> dict[str,Optional[item]]:
#     if item_id:
#          for i in posts:
#             if i["id"] == item_id:
#                 return {"data":item(**i)}
#          raise HTTPException(status_code=404,detail="Post not found,okak")
#     else:
#         return {"data":None}
        
# @app.post("/posts/",response_model=PostResponse)
# async def create_post(user:Postcreate, db: Session = Depends(get_db)) -> User:
#     db_user = User(name=user.name,age=user.age)
#     db.ad(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user