from fastapi import APIRouter, HTTPException
from pydantic import BaseModel



router = APIRouter(#prefix="/users",
                   tags=["users"], # Agrupar en documentación
                   responses={404: {"msg": "No encontrado"}})


# Conceptos importantes: 
# Path -> Para parámetros fijos Y Query -> Para parámetros dinámicos o cuando no son necesarios para la petición
# Si algo salió mal → raise. Si todo salió bien → return
# Router -> enrutamientos para el main
# response_model=User -> lo que se espera que retorne
#===================================
#============== Get ================
# def obtener_listado_objetos(objeto):
#     listado_objetos = sesion.query(objeto).all()
#     if len(listado_objetos) > 0:
#         return listado_objetos


#listado_users_bd = obtener_listado_objetos(User_bd)


 
# Entidad -> BaseModel para para poder trabajar con el objeto en cualquier formato por ejemplo json
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


class User_bd(BaseModel):
    id: int
    name: str
    username: str
    password: str
    email: str
    phone: str
    website: str


# Instancias
users_list = [ User(id=1, name="Ben", surname="Aravena", url="https://ben.dev", age=23),
               User(id=2, name="Jarad", surname="Higgins", url="https://jarad.dev", age=21),
               User(id=3, name="Jahseh", surname="Onfroy", url="https://jahseh.dev", age=20) ]



# App
# @router.get("/users_bd")
# async def users_bd():
#     return listado_users_bd



# @router.get("/users_bd/{id}", response_model=User_bd, status_code=201)
# async def users_bd(id: int):
#     if id < len(listado_users_bd):
#         return listado_users_bd[id]
#     else:
#         raise HTTPException(status_code=416, detail="Fuera de rango")


# Incorrecta manera
@router.get("/usersjson")
async def usersjson():
    return [{ "name": "Ben", "surname": "Aravena", "url": "https://ben.dev", "age": 23},   
            { "name": "Jarad", "surname": "Higgins", "url": "https://jarad.dev", "age": 21},
            { "name": "Jahseh", "surname": "Onfroy", "url": "https://jahseh.dev", "age": 20}]



# Retornamos lista de usuarios
@router.get("/users") # Tiene prefijo -> "/..."
async def users():
    return users_list


# Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)


# Query -> ?id=1  -> &name='Ben'= + parámetros
@router.get("/user/")
async def user(id: int, name: str):
    return search_user(id)



#===================================
#============== Post ===============
@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=409, detail="El usuario ya existe")
    
    users_list.append(user)
    return user


#===================================
#============== Put ================
@router.put("/user/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        raise HTTPException(status_code=404, detail="No se ha encontrado el usuario")
    else:
        return user



#===================================
#============== Delete =============
@router.delete("/userdel/{id}")
async def userdel(id: int):
    found = False
    for index, saved_user  in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        raise HTTPException(status_code=409, detail="El usuario no ha sido eliminado")



@router.delete("/user/{id}")
async def user(id: int):
    user_found = search_user(id)
    if type(user_found) == User:
        users_list.remove(user_found)
    else:
        raise HTTPException(status_code=409, detail="El usuario no ha sido eliminado")
    


# users_list.clear() -> vacía la lista
@router.delete("/user_all/")
async def user_all():
    if users_list != "":
        while users_list:
            users_list.pop()
    else:
        return {"Error: ": "No hay elementos en esta lista"}

#===================================
#============== Patch =============



"""
@app.delete("/user/{id}")
async def delete_user(id: int):
    return {"message": f"Intentando eliminar usuario {id}"}


@app.delete("/user/{id}")
async def userdel(id: int):
    if type(search_user(id)) == User:
        del users_list(id)
    else:
        return {"Error": "Algo salió mal"}

"""


# A simple method
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except: 
        return {"Error": "no se ha encontrado el usuario"}
    