from fastapi import FastAPI
# from database import create_database
from .routers import equipment, muscle_groups, exercises, sets


app = FastAPI(
    version="0.0.1",
    title="Workout Tracker API",
    description="A simple API to track workouts",
    # lifespan=create_database

)


app.include_router(equipment.router)
app.include_router(muscle_groups.router)
app.include_router(exercises.router)
app.include_router(sets.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
