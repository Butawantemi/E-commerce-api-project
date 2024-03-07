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
from .routes import product, user, auth





models.Base.metadata.create_all(bind=engine)

app = FastAPI()

 


     
     
app.include_router(product.router)  
app.include_router(user.router) 
app.include_router(auth.router) 

@app.get("/")
def root():
    return {"Hello Word!"} 


