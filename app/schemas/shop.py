from pydantic import BaseModel
from datetime import datetime


class ShopBase(BaseModel):
    name: str
    assistant_name: str = "SofIA"
    phone: str | None = None
    address: str | None = None
    timezone: str = "America/Bogota"
    prompt: str | None = None


class ShopCreate(ShopBase):
    pass


class ShopUpdate(BaseModel):
    name: str | None = None
    assistant_name: str | None = None
    phone: str | None = None
    address: str | None = None
    timezone: str | None = None
    prompt: str | None = None


class Shop(ShopBase):
    id: str
    created_at: datetime

    model_config = {"from_attributes": True}
