from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel, create_engine, Session
from logger.logger import Logger
from utils.key import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
from contextlib import asynccontextmanager
from fastapi import FastAPI
from populate import populate_db
logger = Logger(__name__)

connection_string = f"postgresql+psycopg2://{
    POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(connection_string)

Base = declarative_base()


@asynccontextmanager
async def create_database(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    try:
        populate_db()
        yield
    finally:
        SQLModel.metadata.drop_all(engine)


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
