from fastapi import APIRouter, HTTPException
from app.database.supabase import get_client
from app.repositories.appointment_repo import AppointmentRepository
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, Appointment
from datetime import datetime

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("/{shop_id}")
async def list_appointments(shop_id: str, date_from: str | None = None, date_to: str | None = None):
    db = get_client()
    repo = AppointmentRepository(db)
    df = datetime.fromisoformat(date_from) if date_from else None
    dt = datetime.fromisoformat(date_to) if date_to else None
    return repo.list_by_shop(shop_id, df, dt)


@router.get("/{shop_id}/today")
async def list_today(shop_id: str):
    db = get_client()
    repo = AppointmentRepository(db)
    return repo.list_today(shop_id)


@router.post("/")
async def create_appointment(data: AppointmentCreate):
    db = get_client()
    repo = AppointmentRepository(db)
    conflict = repo.check_conflict(data.barber_id, data.start_datetime, data.end_datetime)
    if conflict:
        raise HTTPException(status_code=409, detail="Conflicto de horario")
    return repo.create(data)


@router.patch("/{appointment_id}")
async def update_appointment(appointment_id: str, data: AppointmentUpdate):
    db = get_client()
    repo = AppointmentRepository(db)
    appt = repo.get_by_id(appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return repo.update(appointment_id, data)


@router.delete("/{appointment_id}")
async def cancel_appointment(appointment_id: str):
    db = get_client()
    repo = AppointmentRepository(db)
    appt = repo.get_by_id(appointment_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return repo.cancel(appointment_id)
