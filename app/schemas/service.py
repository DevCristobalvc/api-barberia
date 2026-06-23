from pydantic import BaseModel


class ServiceBase(BaseModel):
    shop_id: str
    name: str
    duration: int  # minutes
    price: float


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: str | None = None
    duration: int | None = None
    price: float | None = None


class Service(ServiceBase):
    id: str

    model_config = {"from_attributes": True}
