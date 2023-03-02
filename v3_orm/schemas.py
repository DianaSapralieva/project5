from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserPy(BaseModel):
    email:EmailStr
    password:str

class User_Response(UserPy):
    id: str
    created_at: datetime
    class Config:
        orm_mode=True    

#Pydentic schema for post body validation
class BlogPostPy(BaseModel):
    title:str
    content:str
    published: bool=True
    writer_id: int


#Pydentic schema BlogPost Response 
class BlogPost_Response(BlogPostPy):
    id: int
    created_at: datetime
    #writer:User_Response
    class Config:
        orm_mode=True


     


