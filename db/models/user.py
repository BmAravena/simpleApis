from pydantic import BaseModel



# Entidad -> BaseModel para para poder trabajar con el objeto en cualquier formato por ejemplo json
class User(BaseModel):
    id: str | None = None
    username: str
    email: str
















class User_bd(BaseModel):
    id: int
    name: str
    username: str
    password: str
    email: str
    phone: str
    website: str
