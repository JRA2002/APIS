#my second api
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext

ALGORITHM = "HS256"
SECRET_KEY = "8488848jjjujh40ojfndfd$1212"
ACCESS_TOKEN_EXPIRED_MINUTES = 30

class Token(BaseModel):
    access_token: str
    type_token: str

class TokenData(BaseModel):
    username:str

class User(BaseModel):
    username: str
    email: str

class UserInDb(User):
    password:str

db = {
    "javier":{
        "username": "javier",
        "email": "javier@admin.com",
        "hashed_password":'$2b$12$ISuhZirZoIBqzlYbnyRlleuH28Qptbd4RbV9nJKbo3Uxj/kKNAWH2'
    }
}

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
token_oauth2 = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

async def verify_password(plain_password, hashed_password):
    return pwd.verify(plain_password, hashed_password)

async def get_password_hash(plain_password):
    return pwd.hash(plain_password)



@app.get('/', tags=['home'])
async def home():
    try:
        return 'YOU ARE HOME NOW'
    except:
        return 'ERROR OCURRED'
    

