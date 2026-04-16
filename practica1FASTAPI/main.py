from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Jugador(BaseModel):
    nombre: str
    posicion: str
    dorsal: int
    equipo: str
    titular: bool = True


@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de jugadores de futbol"}


@app.get("/jugadores/{jugador_id}")
def get_jugador(jugador_id: int):
    return {
        "jugador_id": jugador_id,
        "mensaje": "Informacion del jugador",
    }


@app.post("/jugadores/")
def create_jugador(jugador: Jugador):
    return {"mensaje": "Jugador creado exitosamente", "jugador": jugador}


@app.put("/jugadores/{jugador_id}")
def update_jugador(jugador_id: int, jugador: Jugador):
    return {"mensaje": f"Jugador {jugador_id} actualizado", "jugador": jugador}


@app.delete("/jugadores/{jugador_id}")
def delete_jugador(jugador_id: int):
    return {"mensaje": f"Jugador {jugador_id} eliminado"}
