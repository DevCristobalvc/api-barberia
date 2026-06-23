from supabase import Client
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerRepository:
    def __init__(self, db: Client):
        self.db = db
        self.table = "customers"

    def get_by_id(self, customer_id: str) -> dict | None:
        result = self.db.table(self.table).select("*").eq("id", customer_id).single().execute()
        return result.data

    def get_by_phone(self, shop_id: str, phone: str) -> dict | None:
        result = (
            self.db.table(self.table)
            .select("*")
            .eq("shop_id", shop_id)
            .eq("phone", phone)
            .single()
            .execute()
        )
        return result.data

    def search(self, shop_id: str, query: str) -> list[dict]:
        result = (
            self.db.table(self.table)
            .select("*")
            .eq("shop_id", shop_id)
            .or_(f"name.ilike.%{query}%,phone.ilike.%{query}%,notes.ilike.%{query}%")
            .order("name")
            .execute()
        )
        return result.data or []

    def list_by_shop(self, shop_id: str) -> list[dict]:
        result = self.db.table(self.table).select("*").eq("shop_id", shop_id).order("name").execute()
        return result.data or []

    def create(self, data: CustomerCreate) -> dict:
        result = self.db.table(self.table).insert(data.model_dump()).execute()
        return result.data[0]

    def update(self, customer_id: str, data: CustomerUpdate) -> dict:
        payload = {k: v for k, v in data.model_dump().items() if v is not None}
        result = self.db.table(self.table).update(payload).eq("id", customer_id).execute()
        return result.data[0]

    def increment_visits(self, customer_id: str, visit_date: str) -> None:
        customer = self.get_by_id(customer_id)
        if customer:
            self.db.table(self.table).update({
                "visits": (customer.get("visits") or 0) + 1,
                "last_visit": visit_date
            }).eq("id", customer_id).execute()
