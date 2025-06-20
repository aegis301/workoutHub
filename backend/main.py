from fastapi import FastAPI

from .database import create_database
from .routers import equipment, exercises, muscle_groups, sets

app = FastAPI(
    version="0.1.0",
    title="WorkoutHub API",
    description="""
    # WorkoutHub API
    
    A comprehensive workout tracking API that helps you log and analyze your fitness journey.
    
    ## Features
    
    * **Equipment Management**: Track gym equipment and body weight exercises
    * **Exercise Database**: Comprehensive exercise library with muscle group targeting
    * **Workout Logging**: Record sets with weight, reps, RPE, and notes
    * **Muscle Group Analytics**: Hierarchical muscle group organization
    * **Performance Tracking**: Historical data analysis and progress monitoring
    
    ## Data Format
    
    This API returns data in **MessagePack format** for efficient binary serialization.
    All datetime fields are serialized as ISO 8601 strings.
    
    ## Authentication
    
    Currently no authentication is required (development mode).
    
    ## Rate Limiting
    
    No rate limiting is currently implemented.
    """,
    contact={
        "name": "WorkoutHub Support",
        "email": "support@workouthub.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=create_database,
    docs_url="/docs",
    redoc_url="/redoc",
)


app.include_router(equipment.router)
app.include_router(muscle_groups.router)
app.include_router(exercises.router)
app.include_router(sets.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
