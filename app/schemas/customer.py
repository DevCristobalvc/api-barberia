from pydantic import BaseModel
from datetime import datetime


class CustomerBase(BaseModel):
    shop_id: str
    name: str
    phone: str
    notes: str | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: str | None = None
    notes: str | None = None


class Customer(CustomerBase):
    id: str
    visits: int = 0
    last_visit: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
