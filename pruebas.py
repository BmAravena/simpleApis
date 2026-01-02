



"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = f'mysql+mysqlconnector://root:@localhost:3306/usuarios_practice'
motor_db = create_engine(DATABASE_URL)
Session = sessionmaker(bind=motor_db)
sesion = Session()



class User_bd(BaseModel):
    name: str
    username: str
    password: str
    email: str
    phone: str
    website: str


def obtener_listado_objetos(objeto):
    listado_objetos = sesion.query(objeto).all()
    if len(listado_objetos) > 0:
        return listado_objetos

listado_users_bd = obtener_listado_objetos(User_bd)
for usuario in listado_users_bd:
    pass


# App
app = FastAPI()
router = APIRouter()
@router.get("/users_bd")
async def users_bd():
    return listado_users_bd



"""