from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from dependencies import get_db
from models import Cliente, Coche, Servicio
import schemas


app = FastAPI(title="API de Coches")


@app.get("/")
async def read_root():
    return {"mensaje": "Bienvenido a la API de coches con FastAPI y SQLAlchemy de Javier Pozo"}


@app.post("/clientes/", response_model=schemas.ClienteResponse)
async def create_cliente(cliente: schemas.ClienteCreate, db: AsyncSession = Depends(get_db)):
    db_cliente = Cliente(**cliente.model_dump())
    db.add(db_cliente)
    await db.commit()
    await db.refresh(db_cliente)
    return db_cliente


@app.get("/clientes/", response_model=list[schemas.ClienteResponse])
async def list_clientes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cliente))
    return result.scalars().all()


@app.post("/servicios/", response_model=schemas.ServicioResponse)
async def create_servicio(servicio: schemas.ServicioCreate, db: AsyncSession = Depends(get_db)):
    db_servicio = Servicio(**servicio.model_dump())
    db.add(db_servicio)
    await db.commit()
    await db.refresh(db_servicio)
    return db_servicio


@app.get("/servicios/", response_model=list[schemas.ServicioResponse])
async def list_servicios(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Servicio))
    return result.scalars().all()


@app.post("/clientes/{cliente_id}/coches/", response_model=schemas.CocheResponse)
async def create_coche(cliente_id: int, coche: schemas.CocheBase, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cliente).where(Cliente.id == cliente_id))
    cliente = result.scalar_one_or_none()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    db_coche = Coche(**coche.model_dump(), cliente_id=cliente_id)
    db.add(db_coche)
    await db.commit()
    await db.refresh(db_coche)
    return db_coche


@app.get("/coches/", response_model=list[schemas.CocheDetalle])
async def list_coches(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Coche).options(selectinload(Coche.cliente), selectinload(Coche.servicios))
    )
    return result.scalars().all()


@app.get("/coches/{coche_id}", response_model=schemas.CocheDetalle)
async def read_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Coche).where(Coche.id == coche_id).options(selectinload(Coche.cliente), selectinload(Coche.servicios))
    )
    coche = result.scalar_one_or_none()
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")
    return coche


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


@app.delete("/coches/{coche_id}")
async def delete_coche(coche_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Coche).where(Coche.id == coche_id))
    coche = result.scalar_one_or_none()
    if not coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    await db.delete(coche)
    await db.commit()
    return {"mensaje": "Coche eliminado"}