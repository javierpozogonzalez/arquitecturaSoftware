from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from dependencies import get_db
from models import Cliente, Coche, Servicio


app = FastAPI(title="API de Coches")


class CocheCreate(BaseModel):
    marca: str
    modelo: str
    matricula: str
    cliente: str


class CocheResponse(CocheCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ServicioBase(BaseModel):
    nombre: str


class ServicioResponse(ServicioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ClienteBase(BaseModel):
    nombre: str


class ClienteResponse(ClienteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


@app.get("/")
async def read_root():
    return {"mensaje": "Bienvenido a la API de coches con FastAPI y SQLAlchemy de Javier Pozo"}


@app.post("/coches/", response_model=CocheResponse)
async def create_coche(coche: CocheCreate, db: AsyncSession = Depends(get_db)):
    db_coche = Coche(**coche.model_dump())
    db.add(db_coche)
    await db.commit()
    await db.refresh(db_coche)
    return db_coche


@app.get("/coches/", response_model=list[CocheResponse])
async def list_coches(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coche))
    return result.scalars().all()


@app.get("/coches/{coche_id}", response_model=CocheResponse)
async def read_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coche).where(Coche.id == coche_id))
    coche = result.scalar_one_or_none()
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    return coche


@app.put("/coches/{coche_id}", response_model=CocheResponse)
async def update_coche(coche_id: int, coche: CocheCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coche).where(Coche.id == coche_id))
    db_coche = result.scalar_one_or_none()
    if not db_coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    for key, value in coche.model_dump().items():
        setattr(db_coche, key, value)

    await db.commit()
    await db.refresh(db_coche)
    return db_coche


@app.delete("/coches/{coche_id}")
async def delete_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coche).where(Coche.id == coche_id))
    coche = result.scalar_one_or_none()
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    await db.delete(coche)
    await db.commit()
    return {"mensaje": "Coche eliminado"}


@app.post("/clientes/", response_model=ClienteResponse)
async def create_cliente(cliente: ClienteBase, db: AsyncSession = Depends(get_db)):
    db_cliente = Cliente(**cliente.model_dump())
    db.add(db_cliente)
    await db.commit()
    await db.refresh(db_cliente)
    return db_cliente


@app.get("/clientes/", response_model=list[ClienteResponse])
async def list_clientes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cliente))
    return result.scalars().all()


@app.post("/servicios/", response_model=ServicioResponse)
async def create_servicio(servicio: ServicioBase, db: AsyncSession = Depends(get_db)):
    db_servicio = Servicio(**servicio.model_dump())
    db.add(db_servicio)
    await db.commit()
    await db.refresh(db_servicio)
    return db_servicio


@app.get("/servicios/", response_model=list[ServicioResponse])
async def list_servicios(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Servicio))
    return result.scalars().all()


@app.post("/coches/{coche_id}/servicios/{servicio_id}")
async def asignar_servicio(coche_id: int, servicio_id: int, db: AsyncSession = Depends(get_db)):
    res_coche = await db.execute(
        select(Coche).where(Coche.id == coche_id).options(selectinload(Coche.servicios))
    )
    coche = res_coche.scalar_one_or_none()
    
    res_servicio = await db.execute(select(Servicio).where(Servicio.id == servicio_id))
    servicio = res_servicio.scalar_one_or_none()

    if not coche or not servicio:
        raise HTTPException(status_code=404, detail="No encontrado")

    coche.servicios.append(servicio)
    await db.commit()
    return {"mensaje": "Servicio vinculado con éxito"}