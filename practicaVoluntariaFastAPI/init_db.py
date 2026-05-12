import asyncio

from database import Base, engine
from models import Cliente, Coche, Servicio


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())