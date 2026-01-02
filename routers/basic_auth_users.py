from fastapi import FastAPI, APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# OAuth2PasswordBearer -> gestionar autenticación (user-password)
# OAuth2PasswordRequestForm -> la forma en que se enviarán a la api los criterios de autenticación, forma en que se va a capturar
# tokenUrl="login" -> Url que se va a encargar de gestionar la autenticación

router = APIRouter()
# 
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "ben": {
        "username": "ben",
        "full_name": "benjamin aravena",
        "email": "ben@gmail.com",
        "disabled": False,
        "password": "123456"
    },
    "jarad": {
        "username": "jarad",
        "full_name": "jarad higgins",
        "email": "jarad999@gmail.com",
        "disabled": True,
        "password": "654321"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username]) # ** -> varios parámetros
    

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) # ** -> varios parámetros


# Funcional pero no esta siendo utilizada
def create_user(user_db: UserDB):
    return {
        "username": user_db.username,
        "fullname": user_db.full_name,
        "email": user_db.email,
        "disabled": user_db.disabled
    }


@router.get("/user_db")
async def users_bd(username: str):
    return search_user(username)


# Criterio de dependencia /  no esta expuesto en la api 
# current_user -> Depende del sistema de autenticación oauth2
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Credenciales de autenticación inválidas", 
                            headers={"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Usuario inactivo")
    
    return user


# autenticar -> operaciones -> autorizacion(¿qué puedo hacer?) -> dependencia estar autenticado o no con el usuario que pueda
# realizar determinadas operaciones
@router.post("/loginbasic", status_code=status.HTTP_200_OK)
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")

    return {"access Token": user.username, "token_type": "bearer"}


# me -> depende de current_user
@router.get("/usersbasic/me")
async def me(user: User = Depends(current_user)):
    return user

