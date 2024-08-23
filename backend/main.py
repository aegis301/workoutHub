from fastapi import FastAPI
from database import create_database

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_database()


@app.get("/")
async def root():
    return {"message": "Hello World"}
