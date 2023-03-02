from fastapi import FastAPI, Body, Response, status, HTTPException, Depends
from pydantic import BaseModel # Schema 
from typing import Optional
from typing import List
from . import models, schemas # the (.) means current model
from .database import database_engine, get_db # the (.) means current folder
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


# Create the table if they do not exit yet
models.Base.metadata.create_all(bind=database_engine)

# pydantic schema
# class BlogPost(BaseModel):
#     title:str
#     content:str
#     author:str
#     rating:Optional[int] = None
#     published:bool = True

app = FastAPI() #app is the name of the application. We instantiate the class FastAPI


################                 ############
################ END POINTS CODE ############


#### GET operation#####
@app.get("/posts", response_model=List[schemas.BlogPost_Response]) # the @ add extra functionalities to an existing function. code = ENDPOINT of the API using GET
def get_posts(db:Session=Depends(get_db)):
    all_posts=db.query(models.BlogPost).all()
    
    return all_posts


####### POST/CREATE operation #######
@app.post("/posts", response_model=schemas.BlogPost_Response,status_code=status.HTTP_201_CREATED) # decorator + status as a parameter
def create_posts(post_body:schemas.BlogPostPy, db:Session=Depends(get_db)):
   try:
         new_post=models.BlogPost(**post_body.dict())
         db.add(new_post)
         db.commit()
         db.refresh(new_post)
         # status_code=status.HTTP_201_CREATED
         return  new_post 
   except IntegrityError as err:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                           detail=f"Foregn key violation with writer_id:{post_body.writer_id}")
       


######### How to READ ONE SPECIFIC post (use the id) #############
@app.get("/posts/{id_param}", response_model=schemas.BlogPost_Response) # the @ add extra functionalities to an existing function. code = ENDPOINT of the API using GET
def get_post(id_param: int, db: Session=Depends(get_db)):
    corresponding_post=db.query(models.BlogPost).filter(models.BlogPost.id==id_param).first()
    if not corresponding_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"No corresponding post was found for id {id_param}")
    return corresponding_post


######## DELETE a specific post (using the id of the blogpost without the INDEX) #######
@app.delete("/posts/{id_param}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id_param: int,db: Session=Depends(get_db)):
    corresponding_post=db.query(models.BlogPost).filter(models.BlogPost.id==id_param).first()
    if not corresponding_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"No corresponding post was found for id {id_param}")
    db.delete(corresponding_post)
    db.commit() 
    return Response(status_code= status.HTTP_204_NO_CONTENT)

######## post that REPLACE/UPDATE post with request body ########
@app.put('/posts/{id_param}',response_model=schemas.BlogPost_Response)
def update_post(id_param:int, post_body:schemas.BlogPostPy, db:Session=Depends(get_db)):
    try:
        query_post=db.query(models.BlogPost).filter(models.BlogPost.id==id_param)
        if not query_post.first():
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"No corresponding post was found for id {id_param}")
        query_post.update(post_body.dict())
        db.commit()
        return query_post.first()
    except IntegrityError as err:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Foregn key violation with writer_id:{post_body.writer_id}")
    
#################User##############################


#### GET operation#####
@app.get("/users", response_model=List[schemas.User_Response]) # the @ add extra functionalities to an existing function. code = ENDPOINT of the API using GET
def get_posts(db:Session=Depends(get_db)):
    all_posts=db.query(models.User).all()
    
    return all_posts


####### POST/CREATE operation #######
@app.post("/users", response_model=schemas.User_Response,status_code=status.HTTP_201_CREATED) # decorator + status as a parameter
def create_posts(post_body:schemas.UserPy, db:Session=Depends(get_db)):
   try:
         new_post=models.User(**post_body.dict())
         db.add(new_post)
         db.commit()
         db.refresh(new_post)
         # status_code=status.HTTP_201_CREATED
         return  new_post 
   except IntegrityError as err:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                           detail=f"Foregn key violation with writer_id:{post_body.writer_id}")
       


######### How to READ ONE SPECIFIC post (use the id) #############
@app.get("/users/{id_param}", response_model=schemas.User_Response) # the @ add extra functionalities to an existing function. code = ENDPOINT of the API using GET
def get_post(id_param: int, db: Session=Depends(get_db)):
    corresponding_post=db.query(models.User).filter(models.User.id==id_param).first()
    if not corresponding_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"No corresponding post was found for id {id_param}")
    return corresponding_post


######## DELETE a specific post (using the id of the blogpost without the INDEX) #######
@app.delete("/users/{id_param}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id_param: int,db: Session=Depends(get_db)):
    corresponding_post=db.query(models.User).filter(models.User.id==id_param).first()
    if not corresponding_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"No corresponding post was found for id {id_param}")
    db.delete(corresponding_post)
    db.commit() 
    return Response(status_code= status.HTTP_204_NO_CONTENT)

######## post that REPLACE/UPDATE post with request body ########
@app.put('/users/{id_param}',response_model=schemas.User_Response)
def update_post(id_param:int, post_body:schemas.UserPy, db:Session=Depends(get_db)):
    try:
        query_post=db.query(models.User).filter(models.User.id==id_param)
        if not query_post.first():
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"No corresponding post was found for id {id_param}")
        query_post.update(post_body.dict())
        db.commit()
        return query_post.first()
    except IntegrityError as err:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Foregn key violation with writer_id:{post_body.writer_id}")
    
   