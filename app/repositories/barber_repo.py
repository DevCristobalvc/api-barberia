from supabase import Client
from app.schemas.barber import BarberCreate, BarberUpdate


class BarberRepository:
    def __init__(self, db: Client):
        self.db = db
        self.table = "barbers"

    def get_by_id(self, barber_id: str) -> dict | None:
        result = self.db.table(self.table).select("*, barber_services(service_id, services(name))").eq("id", barber_id).single().execute()
        return result.data

    def list_by_shop(self, shop_id: str, active_only: bool = True) -> list[dict]:
        query = self.db.table(self.table).select("*, barber_services(service_id, services(name))").eq("shop_id", shop_id)
        if active_only:
            query = query.eq("active", True)
        result = query.order("name").execute()
        return result.data or []

    def create(self, data: BarberCreate) -> dict:
        result = self.db.table(self.table).insert(data.model_dump()).execute()
        return result.data[0]

    def update(self, barber_id: str, data: BarberUpdate) -> dict:
        payload = {k: v for k, v in data.model_dump().items() if v is not None}
        result = self.db.table(self.table).update(payload).eq("id", barber_id).execute()
        return result.data[0]

    def get_schedule(self, barber_id: str) -> list[dict]:
        result = self.db.table("barber_schedules").select("*").eq("barber_id", barber_id).execute()
        return result.data or []

    def get_blocked_slots(self, barber_id: str) -> list[dict]:
        result = self.db.table("blocked_slots").select("*").eq("barber_id", barber_id).execute()
        return result.data or []
