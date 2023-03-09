from typing import List

from pydantic import BaseModel, HttpUrl


class Movie(BaseModel):
    movie_id: int
    title: str
    genre: str
    imbd_id: int
    tmdb_id: int
    url: HttpUrl
    rating_count: int
    rating_average: float
    poster_path: HttpUrl


class Movies(BaseModel):
    movies: List[Movie] = []
