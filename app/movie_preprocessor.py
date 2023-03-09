import time

import pandas as pd
import requests
from pandas import DataFrame
from tqdm import tqdm

from config import TMDB_API_KEY


def add_poster(dataframe: DataFrame) -> DataFrame:
    """
    데이터 프레임의 tmdb_id 값으로부터 영화 포스터 이미지 정보 추출 및 추가
    @param dataframe: 영화 포스터 이미지 정보를 추가할 데이터 프레임
    @return: 영화 포스터 이미지가 추가된 데이터 프레임
    """
    for i, row in tqdm(dataframe.iterrows(), total=dataframe.shape[0]):
        tmdb_id = row["tmdbId"]
        tmdb_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}&language=en-US"

        result = requests.get(url=tmdb_url)

        try:
            dataframe.at[i, "poster_path"] = "https://image.tmdb.org/t/p/original" + result.json()["poster_path"]
            time.sleep(0.1)
        except (TypeError, KeyError) as e:
            dataframe.at[i, "poster_path"] = "https://image.tmdb.org/t/p/original/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg"

    return dataframe


def add_ratings(dataframe: DataFrame) -> DataFrame:
    """
    ratings.csv 데이터 셋으로부터 영화 평점 정보 추출 및 추가
    @param dataframe: 영화 평점 정보를 추가할 데이터 프레임
    @return: 영화 평점 총 갯수 및 평점의 평균값
    """
    ratings_dataframe = pd.read_csv("data/ratings.csv")

    ratings_dataframe["movieId"] = ratings_dataframe["movieId"].astype(str)

    agg_ratings = ratings_dataframe.groupby("movieId").agg(
        rating_count=("rating", "count"),
        rating_average=("rating", "mean")
    ).reset_index()

    result = dataframe.merge(agg_ratings, on="movieId")

    return result


def get_url(imbd_id: str) -> str:
    """
    데이터 프레임의 imbd_id 값을 맵핑하여 url 형태로 반환
    @param imbd_id: https://www.imbd.com 페이지에서 영화를 구분하는 ID 값
    @return: url
    """
    return f"http://www.imdb.com/title/tt{imbd_id}"


if __name__ == "__main__":
    movies = pd.read_csv("data/movies.csv")
    links = pd.read_csv("data/links.csv", dtype=str)

    movies["movieId"] = movies["movieId"].astype(str)

    result = movies.merge(links, on="movieId", how="left")
    result["url"] = result["imdbId"].apply(lambda imbd_id: get_url(imbd_id=imbd_id))

    result = add_ratings(dataframe=result)

    result["poster_path"] = None
    result = add_poster(dataframe=result)

    result.to_csv(path_or_buf="data/result.csv")
