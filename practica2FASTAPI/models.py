from sqlalchemy import Column, Integer, String

from database import Base


class Coche(Base):
    __tablename__ = "coches"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, index=True)
    modelo = Column(String, index=True)
    matricula = Column(String, unique=True, index=True)
    cliente = Column(String, index=True)