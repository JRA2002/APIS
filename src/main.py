from fastapi import FastAPI, Body, Query, Path
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from pydantic import BaseModel, Field, field_validator
from typing import Optional,List
import datetime
from src.routers.movie_router import movie_router

app = FastAPI()
app.include_router(router=movie_router)
app.title = 'mi first app with fast-api'








