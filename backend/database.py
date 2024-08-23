from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel, create_engine
from logger.logger import Logger
from utils.key import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB

logger = Logger(__name__)

connection_string = f"postgresql+psycopg2://{
    POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(connection_string)

Base = declarative_base()


def create_database():
    SQLModel.metadata.create_all(engine)