from fastapi import FastAPI, APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone 
import hashlib


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "e44a957fc9f06c1a22942d95a8aeb3b4205e4f342fc716a87a09731a933bdda7"
# openssl rand -hex 32 -> Generar pass

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])
#crypt = CryptContext(schemes=["bcrypt_sha256"])

#bcrypt_sha256

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str

#"password": "$2a$12$YfI3ySAJ82mKxl7Io3qh2.NaHWADK/19UYJT7UiEFhM.w2vD/hgRa"
users_db = {
    "ben": {
        "username": "ben",
        "full_name": "benjamin aravena",
        "email": "ben@gmail.com",
        "disabled": False,
        "password": "$2a$12$B2Gq.Dps1WYf2t57eiIKjO4DXC3IUMUXISJF62bSRiFfqMdOI2Xa6"
    },
    "jarad": {
        "username": "jarad",
        "full_name": "jarad higgins",
        "email": "jarad999@gmail.com",
        "disabled": True,
        "password": "$2a$12$SduE7dE.i3/ygwd0Kol8bOFvEABaoOOlC8JsCSr6wpwB4zl5STU4S"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) # ** -> varios parámetros


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) # ** -> varios parámetros


async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Credenciales de autenticación inválidas", 
                headers={"WWW-Authenticate": "Bearer"})

    try: 
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")

        if username is None:
            raise exception
        

    except JWTError:
        raise exception

    return search_user(username)


        
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario inactivo")
    
    return user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(form: OAuth2PasswordRequestForm = Depends()):

    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
 

    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    

    return {"access Token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user