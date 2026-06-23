from datetime import datetime, timedelta, date
from langchain_core.tools import tool
from app.database.supabase import get_client
from app.repositories.appointment_repo import AppointmentRepository
from app.repositories.barber_repo import BarberRepository
import pytz


@tool
def get_availability(shop_id: str, service_duration: int, date_str: str, barber_id: str | None = None) -> dict:
    """
    Consulta la disponibilidad de horarios para un servicio.
    Args:
        shop_id: ID de la barbería
        service_duration: duración del servicio en minutos
        date_str: fecha en formato YYYY-MM-DD
        barber_id: ID del barbero (opcional, si None busca en todos)
    Returns:
        dict con slots disponibles por barbero
    """
    db = get_client()
    barber_repo = BarberRepository(db)
    appt_repo = AppointmentRepository(db)

    target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    weekday = target_date.weekday()

    barbers = [barber_repo.get_by_id(barber_id)] if barber_id else barber_repo.list_by_shop(shop_id)
    barbers = [b for b in barbers if b]

    availability = {}

    for barber in barbers:
        schedule = barber_repo.get_schedule(barber["id"])
        day_schedule = next((s for s in schedule if s["weekday"] == weekday), None)

        if not day_schedule:
            continue

        start_hour = int(day_schedule["start_time"].split(":")[0])
        start_min = int(day_schedule["start_time"].split(":")[1])
        end_hour = int(day_schedule["end_time"].split(":")[0])
        end_min = int(day_schedule["end_time"].split(":")[1])

        day_start = datetime.combine(target_date, datetime.min.time().replace(hour=start_hour, minute=start_min))
        day_end = datetime.combine(target_date, datetime.min.time().replace(hour=end_hour, minute=end_min))

        existing = appt_repo.list_by_barber(
            barber["id"],
            datetime.combine(target_date, datetime.min.time()),
            datetime.combine(target_date, datetime.max.time()),
        )
        blocked = barber_repo.get_blocked_slots(barber["id"])

        busy_intervals = [(datetime.fromisoformat(a["start_datetime"]), datetime.fromisoformat(a["end_datetime"])) for a in existing]
        for b in blocked:
            b_start = datetime.fromisoformat(b["start_datetime"])
            b_end = datetime.fromisoformat(b["end_datetime"])
            if b_start.date() <= target_date <= b_end.date():
                busy_intervals.append((b_start, b_end))

        slots = []
        current = day_start
        slot_duration = timedelta(minutes=service_duration)

        while current + slot_duration <= day_end:
            slot_end = current + slot_duration
            conflict = any(s < slot_end and e > current for s, e in busy_intervals)
            if not conflict:
                slots.append(current.strftime("%H:%M"))
            current += timedelta(minutes=30)

        if slots:
            availability[barber["name"]] = {
                "barber_id": barber["id"],
                "slots": slots
            }

    return availability
