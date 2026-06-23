from datetime import datetime, date
from supabase import Client
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate


class AppointmentRepository:
    def __init__(self, db: Client):
        self.db = db
        self.table = "appointments"

    def get_by_id(self, appointment_id: str) -> dict | None:
        result = self.db.table(self.table).select("*").eq("id", appointment_id).single().execute()
        return result.data

    def list_by_shop(self, shop_id: str, date_from: datetime | None = None, date_to: datetime | None = None) -> list[dict]:
        query = self.db.table(self.table).select("*").eq("shop_id", shop_id)
        if date_from:
            query = query.gte("start_datetime", date_from.isoformat())
        if date_to:
            query = query.lte("start_datetime", date_to.isoformat())
        result = query.order("start_datetime").execute()
        return result.data or []

    def list_today(self, shop_id: str) -> list[dict]:
        today = date.today()
        start = datetime.combine(today, datetime.min.time()).isoformat()
        end = datetime.combine(today, datetime.max.time()).isoformat()
        result = (
            self.db.table(self.table)
            .select("*, customers(name, phone), barbers(name), services(name, duration, price)")
            .eq("shop_id", shop_id)
            .gte("start_datetime", start)
            .lte("start_datetime", end)
            .neq("status", "cancelled")
            .order("start_datetime")
            .execute()
        )
        return result.data or []

    def list_by_barber(self, barber_id: str, date_from: datetime, date_to: datetime) -> list[dict]:
        result = (
            self.db.table(self.table)
            .select("*")
            .eq("barber_id", barber_id)
            .gte("start_datetime", date_from.isoformat())
            .lte("end_datetime", date_to.isoformat())
            .neq("status", "cancelled")
            .execute()
        )
        return result.data or []

    def create(self, data: AppointmentCreate) -> dict:
        result = self.db.table(self.table).insert(data.model_dump()).execute()
        return result.data[0]

    def update(self, appointment_id: str, data: AppointmentUpdate) -> dict:
        payload = {k: v for k, v in data.model_dump().items() if v is not None}
        result = self.db.table(self.table).update(payload).eq("id", appointment_id).execute()
        return result.data[0]

    def cancel(self, appointment_id: str) -> dict:
        result = self.db.table(self.table).update({"status": "cancelled"}).eq("id", appointment_id).execute()
        return result.data[0]

    def check_conflict(self, barber_id: str, start: datetime, end: datetime, exclude_id: str | None = None) -> bool:
        query = (
            self.db.table(self.table)
            .select("id")
            .eq("barber_id", barber_id)
            .neq("status", "cancelled")
            .lt("start_datetime", end.isoformat())
            .gt("end_datetime", start.isoformat())
        )
        if exclude_id:
            query = query.neq("id", exclude_id)
        result = query.execute()
        return len(result.data or []) > 0
