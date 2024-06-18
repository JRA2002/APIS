from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse
from src.routers.movie_router import movie_router

app = FastAPI()
app.include_router(prefix='/movies', router=movie_router)
app.title = 'mi first app with fast-api'

@app.middleware('http')
async def http_error_handle(request:Request, call_next) -> Response | JSONResponse:
    print('Middleware is running')
    return await call_next(request)









