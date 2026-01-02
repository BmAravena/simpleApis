from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User_bd(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    username = Column(String(50))
    password = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    website = Column(String(100))


