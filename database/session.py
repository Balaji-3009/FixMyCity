from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List, Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from dotenv import load_dotenv
import os

load_dotenv('.env')
database_url = os.getenv("DATABASE_URL")


URL_DATABASE = database_url

engine = create_engine(URL_DATABASE,pool_size=50,max_overflow=100, pool_timeout=1)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]