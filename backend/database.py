import psycopg2

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from logger.logger import Logger
from utils.key import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_DEFAULT_DB

logger = Logger(__name__)

connection_string = f"postgresql+psycopg2://{
    POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def create_database(db_name):
    try:
        # Connect to the default database
        conn = psycopg2.connect(
            dbname=POSTGRES_DEFAULT_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {db_name};")
        logger.info(f"Database {db_name} created successfully.")
        cursor.close()
        conn.close()
        return True
    except psycopg2.errors.DuplicateDatabase:
        logger.info(f"Database {db_name} already exists.")
        return False
    except Exception as e:
        logger.error(f"Error creating database {db_name}: {e}")
        return False
