from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET_KEY = "5c1c3597244d559cf45e442625dc76c1b9b2589f6fbf6545fd2e2cd1d9f0b0a1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRED_MINUTES = 30

db = {
    'javier' : 
        {
        'username': 'javier',
        'email': 'javier@example.com',
        'hashed_password': '$2b$12$Ab8VgQxKrp3PNH4SKPH.m.mY.4N7mfrngr/iu9W/1Qsot0izfmAXW',
        'disabled': False
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class User(BaseModel):
    username: str
    email: str or None = None
    disabled: bool or None = None

class UserInDb(User):
    hashed_password: str

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_data = db[username]
    return UserInDb(**user_data)

def authenticated_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = expires_delta + datetime.now()
    else:
        expire = expires_delta + timedelta(minutes=15)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail='Not validate Credentials',
                                         headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            return credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        return credential_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        return credential_exception
    return user

async def get_current_active_user(current_user: UserInDb = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive User')
    return current_user

@app.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticated_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password',
                            headers={'WWW-Authenticate': 'Bearer'})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRED_MINUTES)
    access_token = create_access_token(data={'sub': user.username},
                                       expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.get('/users/readme', response_model=User)
async def read_users(current_user: User = Depends(get_current_active_user)):
    return current_user

pwd = verify_password('admin', '$2b$12$Ab8VgQxKrp3PNH4SKPH.m.mY.4N7mfrngr/iu9W/1Qsot0izfmAXW')
print(pwd)