import json

from fastapi import FastAPI
from src.api.movie_routes import router as movie_router

app = FastAPI()

app.include_router(movie_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}