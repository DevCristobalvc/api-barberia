from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class AppointmentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"
    no_show = "no_show"


class AppointmentSource(str, Enum):
    whatsapp = "whatsapp"
    dashboard = "dashboard"
    api = "api"


class AppointmentBase(BaseModel):
    shop_id: str
    barber_id: str
    customer_id: str
    service_id: str
    start_datetime: datetime
    end_datetime: datetime
    notes: str | None = None
    source: AppointmentSource = AppointmentSource.dashboard


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    barber_id: str | None = None
    start_datetime: datetime | None = None
    end_datetime: datetime | None = None
    status: AppointmentStatus | None = None
    notes: str | None = None


class Appointment(AppointmentBase):
    id: str
    status: AppointmentStatus = AppointmentStatus.pending
    created_at: datetime

    model_config = {"from_attributes": True}


class AppointmentWithDetails(Appointment):
    customer_name: str | None = None
    customer_phone: str | None = None
    barber_name: str | None = None
    service_name: str | None = None
    service_duration: int | None = None
    service_price: float | None = None
