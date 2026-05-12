from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from database import Base


coche_servicio_association = Table(
    "coche_servicio",
    Base.metadata,
    Column("coche_id", ForeignKey("coches.id"), primary_key=True),
    Column("servicio_id", ForeignKey("servicios.id"), primary_key=True),
)


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)

    coches = relationship("Coche", back_populates="cliente")


class Coche(Base):
    __tablename__ = "coches"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, index=True)
    modelo = Column(String, index=True)
    matricula = Column(String, unique=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    cliente = relationship("Cliente", back_populates="coches")
    servicios = relationship("Servicio", secondary=coche_servicio_association, back_populates="coches")


class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True)

    coches = relationship("Coche", secondary=coche_servicio_association, back_populates="servicios")