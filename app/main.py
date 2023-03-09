from fastapi import FastAPI

from .models.responses import Movies
from .resolver import get_movies_randomly, get_movies_by_genre_randomly

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/all/")
async def get_all_movies() -> Movies:
    result = get_movies_randomly()
    return result


@app.get("/genres/{genre}")
async def get_movies_by_genre(genre: str) -> Movies:
    result = get_movies_by_genre_randomly(genre=genre)
    return result
