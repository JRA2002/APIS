#my second api
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

class Movie(BaseModel):
    id:int
    name:str
    star:int

app = FastAPI()
movies : List[Movie] = []
@app.get('/', tags=['home'])
async def home():
    return 'my home'

@app.post('/movie', tags=['movies'])
async def create_movie(movie:Movie) -> List[Movie]:
    movies.append(movie)
    return movies

@app.get('/movie/{id}', tags=['movies'])
async def get_movie(id:int):
    for movie in movies:
        if movie.id == id:
            return movie
    return 'bad ID provided'
@app.put('/movie/{id}', tags=['movies'])
async def update_movie(id:int, movie:Movie) -> List[Movie]:
    for item in movies:
        if item.id == id:
            item.id = movie.id
            item.name = movie.name
            item.star = movie.star
            return movies
    return 'not found'