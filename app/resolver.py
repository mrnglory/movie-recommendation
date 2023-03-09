import pandas as pd

from .models.responses import Movie, Movies


def get_movies_randomly() -> Movies:
    """
    영화 데이터 랜덤 추출 및 반환
    @return: Movies
    """
    movies_dataframe = pd.read_csv("app/data/result.csv")
    movies_dataframe = movies_dataframe.fillna("")

    movies = movies_dataframe.sample(n=10).to_dict("records")

    result = Movies(**{"movies": [Movie(**movie) for movie in movies]})

    return result


def get_movies_by_genre_randomly(genre: str) -> Movies:
    """
    입력된 장르 정보에 대한 영화 데이터 랜덤 추출 및 반환
    @param genre: 영화 장르
    @return: Movies
    """
    movies_dataframe = pd.read_csv("app/data/result.csv")

    movies_by_genre = movies_dataframe[movies_dataframe["genre"].apply(lambda x: genre in x.lower())]

    movies = movies_by_genre.fillna("").sample(n=10).to_dict("records")

    result = Movies(**{"movies": [Movie(**movie) for movie in movies]})

    return result

