from fastapi import APIRouter, HTTPException, status
from database import sesion
from obtener import obtener_listado_objetos
from db.models.user import User
from db.client import db_client
from db.schemes.user import user_scheme, users_scheme
from bson import ObjectId
 

router = APIRouter(prefix="/userdb",
                   tags=["userdb"], # Agrupar en documentación
                   responses={status.HTTP_404_NOT_FOUND: {"msg": "No encontrado"}})


# Conceptos importantes: 
# Path -> Para parámetros fijos Y Query -> Para parámetros dinámicos o cuando no son necesarios para la petición
# Si algo salió mal → raise. Si todo salió bien → return
# Router -> enrutamientos para el main
# response_model=User -> lo que se espera que retorne
#===================================
#============== Get ================
def obtener_listado_objetos(objeto):
    listado_objetos = sesion.query(objeto).all()
    if len(listado_objetos) > 0:
        return listado_objetos


# Instancias
users_list = []

# Get one by id
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))


# Get one by username
@router.get("/{username}")
async def user(username: str):
    user_found = db_client.users.find_one({"username": username})

    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha encontrado el usuario")

    return user_scheme(user_found)

 
# Get all from db
@router.get("/", response_model=list[User])
async def users():
    return users_scheme(db_client.users.find())


def creaUsuario():
    id = int(input("Ingresa la Id: "))
    username = input("Ingresa el nombre de usuario: ")
    email = input("Ingresa el email: ")

    return User(id, username, email)



#===================================
#============== Post ===============
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id
    new_user = user_scheme(db_client.users.find_one({"_id": id}))

    return User(**new_user)



@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):
    # if type(search_user(user.id)) == User:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id
    new_user = user_scheme(db_client.users.find_one({"_id": id}))

    return User(**new_user)



#===================================
#============== Put ================

    
# Put actualiza todo el objeto, para un dato esta patch
@router.put("/", response_model=User)
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)

    except:
        return {"Error": "No se ha actualizado el usuario"}

    return search_user("_id", ObjectId(user.id))
  


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
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El usuario no ha sido eliminado")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def userdel(id: str):

   # user_found = search_user("_id", ObjectId(id))
    user_found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not user_found:
        return {"Error": "No se ha eliminado le usuario"}
    
    # if not (type(user_found) == User):
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no ha sido eliminado")
    
    # db_client.local.users.delete_one(user_found)




@router.delete("/userdb/{id}")
async def user(id: int):
    user_found = search_user("id", id)
    if type(user_found) == User:
        users_list.remove(user_found)
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El usuario no ha sido eliminado")
    


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


# A simple method
def search_user_by_name(username: str):
    try:
        return db_client.users.find_one({"username": username})
    except: 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El usuario con username {username} ya existe")
    

def search_user(field: str, key):

    try:
        user = db_client.users.find_one({field: key})
        return User(**user_scheme(user))
    except: 
        return {"Error": "No se ha encontrado el usuario"}
    


def search_user_by_email(email: str):
    try:
        user = db_client.users.find_one({"username": email})
        return User(**user_scheme(user))
    except: 
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"El usuario con email {email} ya existe")