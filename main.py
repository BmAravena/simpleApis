from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

# uvicorn main:app --reload -> iniciar servidor, --reload es para que los cambios hechos se actualizen en tiempo real
# docs, redoc documentación automatica del código
# Autenticación -> identificarse, que el sistema tenga claro, ¿Quién eres? 
# Autorización ->  Es el proceso de decidir a qué recursos puedes acceder y qué acciones puedes hacer, ¿Qué permisos tienes?

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)

app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

app.mount('/static', StaticFiles(directory='static'), name='JuiceWRLD') # Para exponer recursos estáticos -> imagenes, archivos...


@app.get("/")
async def root():
    return "¡Hola FastApi2!"

#ip/url...
@app.get("/url")
async def url():
    return { "url_curso":"https://mourdev.com/python" }
