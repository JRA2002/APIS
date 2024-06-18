from typing import List
from fastapi import Path, Query, APIRouter
from src.models.movie_model import Movie, MovieCreate, MovieUpdate

movie_router = APIRouter()

movies : List[Movie] = []
@movie_router.get("/", tags=['Movies'])
def get_movies() -> List[Movie]:
    return [movie.model_dump() for movie in movies]

@movie_router.get("/{id}", tags=['Movies'])
def get_movie(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            return movie.model_dump()
    return {}

@movie_router.get("/by_category", tags=['Movies'])
def get_movie_by_category(category: str = Query(min_length=4, max_length=20)) -> Movie | dict:
    for movie in movies:
        if movie.category == category:
            return movie.model_dump()
    return {}

@movie_router.post("/", tags=['Movies'])
def create_movie(movie: MovieCreate) -> List[Movie]:
    movies.append(movie)
    #return [movie.model_dump() for movie in movies]
    return [movie.model_dump() for movie in movies]

@movie_router.put("/{id}", tags=["Movies"])
def update_movie(
    id: int, movie:MovieUpdate
) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.title = movie.title
            item.director = movie.director
            item.year = movie.year
            item.plot = movie.plot
            item.language = movie.language
            item.category = movie.category

    return [movie.model_dump() for movie in movies]

@movie_router.delete("/{id}", tags=["Movies"])
def delete_movie(id: int):
    for movie in movies:
        if movie.id == id:
            movies.remove(movie)
    return movies