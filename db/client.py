from pymongo import MongoClient
from db.datos_de_conexion import user_db, password_db

# Base de datos local
#db_client = MongoClient().local

# Base de datos remota
db_client = MongoClient(f"mongodb+srv://{user_db}:{password_db}@cluster0.mjnrlea.mongodb.net/?appName=Cluster0").test