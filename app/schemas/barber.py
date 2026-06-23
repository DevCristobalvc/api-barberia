from pydantic import BaseModel
from datetime import time


class ScheduleSlot(BaseModel):
    weekday: int  # 0=Monday, 6=Sunday
    start_time: time
    end_time: time


class BarberBase(BaseModel):
    shop_id: str
    name: str
    active: bool = True


class BarberCreate(BarberBase):
    pass


class BarberUpdate(BaseModel):
    name: str | None = None
    active: bool | None = None


class Barber(BarberBase):
    id: str
    services: list[str] = []

    model_config = {"from_attributes": True}
