from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from models import Coche


app = FastAPI(title="API de Coches")


class CocheCreate(BaseModel):
    marca: str
    modelo: str
    matricula: str
    cliente: str


class CocheResponse(CocheCreate):
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
    db_coche = result.scalar_one_or_none()
    if not db_coche:
        raise HTTPException(status_code=404, detail="Coche no encontrado")

    await db.delete(db_coche)
    await db.commit()
    return {"mensaje": "Coche eliminado"}