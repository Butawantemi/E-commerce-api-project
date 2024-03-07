from random import randrange
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from . import database
from .database import get_db, engine
from .routes import post, user, auth





models.Base.metadata.create_all(bind=engine)

app = FastAPI()

 

while True:   
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
        password='123456', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database was connected succesfully")
        break
    except Exception as error:
        print("Database was not connected")
        print("Error", error)
        time.sleep(2)
    
my_post = [{"title":"title of the post", "content":"content of the post", "id":1}, 
        {"title":"My fevourate food", "content":"I like Ugali", "id":2}]

def find_post(id):
    for p in my_post:
      if p["id"] == id:
         return p 
     
def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
         return i
     
     
app.include_router(post.router)  
app.include_router(user.router) 
app.include_router(auth.router) 

""" @app.get("/")
def root():
    return {"Hello Word!"} """


