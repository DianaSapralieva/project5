from fastapi import FastAPI, Body, Response,status,HTTPException
from pydantic import BaseModel #schema
from typing import Optional

def next_id(posts):
   max_id = 0
   for post in posts:
       if post['id'] > max_id:
           max_id = post['id']
   return max_id + 1

def find_posts(given_id):
   for post in my_blog_post:
      if post["id"]==given_id:
         return post
      
def find_post_index(given_id):
    for index, post in enumerate(my_blog_post):
        if post['id'] == given_id:
            return index






class BlogPost(BaseModel):
   title: str
   content: str
   author: str
   rating: Optional[int]=None
   published: bool=True    

app=FastAPI()#app is the name of the application 
my_blog_post=[
        {"id":1,'title': 'First post'},
        {"id":2,'title': 'Second post'},
        {"id":3,'title': 'Third post'}]

@app.get("/posts")#end point using path/and method Get
def get_posts():
   return {"data": my_blog_post}

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(new_post: BlogPost, response: Response):
   post_data=new_post.dict()
   temp_data={"id":next_id(my_blog_post)}
   temp_data.update(post_data)
   my_blog_post.append(temp_data)
   #response.status_code=201
   return {"message":f"new blog posts added with title:{new_post.title} "}


@app.get("/posts/{id_param}")
def get_post(id_param: int, response: Response):
   corresponding_post=find_posts(id_param)
   if not corresponding_post:
      raise HTTPException(
      response.status_code==status.HTTP_404_NOT_FOUND, detail=f"no corrrinponding post was found for id {id_param}"
      )
   return {"data":corresponding_post}


@app.delete("/posts/{id_param}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id_param: int, response: Response):
   corresponding_index=find_post_index(id_param)
   if not corresponding_index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"No corresponding post was found for id {id_param}")
   #remove the element from the list
   my_blog_post.pop(corresponding_index)
   return Response(status_code= status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id_param}", status_code= status.HTTP_200_OK)
def replace_post(id_param: int, updated_post: BlogPost, response: Response):
    #updating logic
    corresponding_index=find_post_index(id_param)
    if not corresponding_index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
              detail=f"No corresponding post was found for id {id_param}")
    #transform the data from the body to a dict
    updated_post_dict=updated_post.dict()
    #add id
    updated_post_dict["id"]=id_param
    #replace my blog posts with updated post dict
    my_blog_post[corresponding_index]=updated_post_dict
    return updated_post_dict
   