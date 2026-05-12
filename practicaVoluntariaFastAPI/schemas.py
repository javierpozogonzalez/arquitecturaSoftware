from pydantic import BaseModel, ConfigDict


class ClienteBase(BaseModel):
    nombre: str


class ClienteCreate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ServicioBase(BaseModel):
    nombre: str


class ServicioCreate(ServicioBase):
    pass


class ServicioResponse(ServicioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CocheBase(BaseModel):
    marca: str
    modelo: str
    matricula: str


class CocheCreate(CocheBase):
    cliente_id: int


class CocheDetalle(CocheBase):
    id: int
    cliente: ClienteResponse | None = None
    servicios: list[ServicioResponse] = []

    model_config = ConfigDict(from_attributes=True)


class CocheResponse(CocheBase):
    id: int
    cliente_id: int

    model_config = ConfigDict(from_attributes=True)
