from sqlalchemy import Column, String, create_engine, Integer, Text, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time

from sqlalchemy import create_engine
engine = create_engine("postgresql://postgres:wennitao@127.0.0.1:5432/bookstore",
    echo=True,
    pool_size=8, 
    pool_recycle=60*30
)

DbSession = sessionmaker(bind=engine)
session = DbSession()