from datetime import datetime, timedelta
from langchain_core.tools import tool
from app.database.supabase import get_client
from app.repositories.appointment_repo import AppointmentRepository
from app.repositories.barber_repo import BarberRepository
from app.repositories.customer_repo import CustomerRepository
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentStatus, AppointmentSource


@tool
def create_booking(
    shop_id: str,
    customer_id: str,
    barber_id: str,
    service_id: str,
    start_datetime: str,
    service_duration: int,
    notes: str | None = None,
    source: str = "whatsapp",
) -> dict:
    """
    Crea una nueva cita.
    Args:
        shop_id: ID de la barbería
        customer_id: ID del cliente
        barber_id: ID del barbero
        service_id: ID del servicio
        start_datetime: fecha y hora de inicio en ISO format (YYYY-MM-DDTHH:MM:SS)
        service_duration: duración en minutos
        notes: notas adicionales
        source: origen de la cita (whatsapp, dashboard, api)
    """
    db = get_client()
    repo = AppointmentRepository(db)

    start = datetime.fromisoformat(start_datetime)
    end = start + timedelta(minutes=service_duration)

    conflict = repo.check_conflict(barber_id, start, end)
    if conflict:
        return {"error": "El horario ya está ocupado. Por favor elige otro."}

    appt = AppointmentCreate(
        shop_id=shop_id,
        customer_id=customer_id,
        barber_id=barber_id,
        service_id=service_id,
        start_datetime=start,
        end_datetime=end,
        notes=notes,
        source=AppointmentSource(source),
    )
    result = repo.create(appt)
    return {"success": True, "appointment_id": result["id"], "start": start.strftime("%d/%m/%Y a las %H:%M")}


@tool
def cancel_booking(appointment_id: str, shop_id: str) -> dict:
    """
    Cancela una cita existente.
    Args:
        appointment_id: ID de la cita
        shop_id: ID de la barbería (para validar)
    """
    db = get_client()
    repo = AppointmentRepository(db)
    appt = repo.get_by_id(appointment_id)

    if not appt or appt["shop_id"] != shop_id:
        return {"error": "Cita no encontrada."}
    if appt["status"] == "cancelled":
        return {"error": "La cita ya estaba cancelada."}

    repo.cancel(appointment_id)
    return {"success": True, "message": "Cita cancelada correctamente."}


@tool
def move_booking(appointment_id: str, new_start_datetime: str, shop_id: str) -> dict:
    """
    Reprograma una cita a otro horario.
    Args:
        appointment_id: ID de la cita
        new_start_datetime: nueva fecha y hora en ISO format
        shop_id: ID de la barbería
    """
    db = get_client()
    repo = AppointmentRepository(db)
    appt = repo.get_by_id(appointment_id)

    if not appt or appt["shop_id"] != shop_id:
        return {"error": "Cita no encontrada."}

    old_start = datetime.fromisoformat(appt["start_datetime"])
    old_end = datetime.fromisoformat(appt["end_datetime"])
    duration = int((old_end - old_start).total_seconds() / 60)

    new_start = datetime.fromisoformat(new_start_datetime)
    new_end = new_start + timedelta(minutes=duration)

    conflict = repo.check_conflict(appt["barber_id"], new_start, new_end, exclude_id=appointment_id)
    if conflict:
        return {"error": "El nuevo horario ya está ocupado. Por favor elige otro."}

    update = AppointmentUpdate(start_datetime=new_start, end_datetime=new_end)
    repo.update(appointment_id, update)

    return {
        "success": True,
        "message": f"Cita reprogramada para el {new_start.strftime('%d/%m/%Y a las %H:%M')}.",
    }


@tool
def list_today(shop_id: str) -> list[dict]:
    """
    Lista las citas del día actual para una barbería.
    Args:
        shop_id: ID de la barbería
    """
    db = get_client()
    repo = AppointmentRepository(db)
    return repo.list_today(shop_id)
