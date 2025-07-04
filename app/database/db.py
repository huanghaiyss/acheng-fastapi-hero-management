from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
from fastapi import Depends
import os

load_dotenv()
sqlite_url = os.getenv("DATABASE_URL")
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

