import psycopg2
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

from ..logger import Logger

logger = Logger(__name__)

load_dotenv()


def check_for_database(db_name: str, user: str, password: str, host: str, port: str) -> bool:
    """Check if the specified database exists, if not, create it."""
    try:
        connection_string = f"postgresql+psycopg2://{
            user}:{password}@{host}:{port}/postgres"
        logger.debug(f"Connecting to database: {connection_string}")
        engine = create_engine(connection_string)
        with engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE {db_name};"))
            logger.info(f"Database {db_name} created.")
            return True
    except psycopg2.errors.DuplicateDatabase:
        logger.info(f"Database {db_name} already exists.")
        return False
    except Exception as e:
        logger.error(f"Error accessing database {db_name}: {e}")
        return False


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

POSTGRES_DB = "workoutHub"


connection_string = f"postgresql+psycopg2://{
    POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
