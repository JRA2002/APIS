import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class Movie(BaseModel):
    id: Optional[int] = None
    title: str
    director: str 
    year: int 
    plot: str 
    language: str 
    category: str

class MovieUpdate(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=3, max_length=10)
    director: str = Field(min_length=4, max_length=20)
    year: int = Field(le=datetime.date.today().year, gt=1900)
    plot: str = Field(min_length=10, max_length=50)
    language: str = Field(min_length=2, max_length=10)
    category: str = Field(min_length=4, max_length=20)

class MovieCreate(BaseModel):
    id: int = Field(gt=0, default=1)
    title: str
    director: str = Field(min_length=4, max_length=20)
    year: int = Field(le=datetime.date.today().year, gt=1900, default=1990)
    plot: str = Field(min_length=10, max_length=50, default='jajajajajajajajjajaj')
    language: str = Field(min_length=2, max_length=10)
    category: str = Field(min_length=4, max_length=20)

    @field_validator('title')
    def validate_title(cls, value):
        if len(value) < 3:
            raise ValueError('VERY SHORT')
        if len(value) > 20:
            raise ValueError('VERY LARGE')
        return value