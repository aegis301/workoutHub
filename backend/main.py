import models.models as models
from fastapi import FastAPI
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


db_dependency = Annotaded(Session, Depends(get_db))


@app.get("/")
async def root():
    return {"message": "Hello World"}
