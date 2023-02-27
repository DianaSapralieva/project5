from fastapi import FastAPI, Body, Response,status,HTTPException
from pydantic import BaseModel #schema
from typing import Optional
import psycopg2 
from psycopg2.extras import RealDictCursor

try:
   connection=psycopg2.connect(
      host="localhost",
      database="reddit_clone",
      user="postgres",
      password="API",
      cursor_factory=RealDictCursor )

   cursor=connection.cursor()
   print("DataBase connection is succesful")
except Exception as error:
   print("DataBase coonection failed")
   print("Error",error)



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
   #writing the sql query
   cursor.execute("SELECT * FROM posts")
   #retrieves all the posts (list)
   database_posts=cursor.fetchall()
   print(database_posts)
   return {"data": database_posts}

@app.put("/posts/{id}")
def update_post_by_id(id: int, post: BlogPost):
    # Convert the ID to a string
    id_str = str(id)
    # Execute the SQL query to update the post with the given ID
    cursor.execute(
        "UPDATE posts SET title = %s, content = %s WHERE id = %s",
        (post.title, post.content, id_str)
    )
    # Commit the transaction
    connection.commit()
    # Get the corresponding row from the DBMS
    row = cursor.fetchone()
    # If no row is found, raise an HTTP Exception
    if row is None:
        raise HTTPException(status_code=404, detail="404 Post not found")
    # Return a success response
    return {"message": "Post updated successfully."}, 200


@app.get("/posts/{id}")
def get_post_by_id(id: int):
    # Convert the ID to a string
    id_str = str(id)
    # Execute the SQL query using the ID parameter
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id_str,))
    # Get the corresponding row from the DBMS
    row = cursor.fetchone()
    # If no row is found, raise an HTTP Exception
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 Post not found")
    # Return the row to the client
    return row

@app.delete("/posts/{id}")
def get_post_by_id(id: int):
    # Convert the ID to a string
    id_str = str(id)
    # Execute the SQL query using the ID parameter
    cursor.execute("DELETE FROM posts WHERE id= %s RETURNING *", (id_str,))
    row = cursor.fetchone()
    # Get the corresponding row from the DBMS
    connection.commit() 
    # If no row is found, raise an HTTP Exception
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 Post not found")
   #remove the element from the list
     # Return a success response
   
    return {"message": "Post deleted successfully."}, Response(status_code=status.HTTP_204_NO_CONTENT) 


@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(new_post: BlogPost):
   cursor.execute("INSERT INTO posts (title, content, author, published, rating) "+
                  "VALUES (%s,%s,%s,%s,%s)RETURNING * ", (new_post.title,new_post.content,new_post.author,new_post.published,new_post.rating))
   new_post=cursor.fetchone()
   connection.commit()#saves changes to the data base
   return {"data":new_post}


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
   