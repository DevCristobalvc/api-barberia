from supabase import Client
from app.schemas.shop import ShopCreate, ShopUpdate


class ShopRepository:
    def __init__(self, db: Client):
        self.db = db
        self.table = "shops"

    def get_by_id(self, shop_id: str) -> dict | None:
        result = self.db.table(self.table).select("*").eq("id", shop_id).single().execute()
        return result.data

    def list_all(self) -> list[dict]:
        result = self.db.table(self.table).select("*").execute()
        return result.data or []

    def create(self, data: ShopCreate) -> dict:
        result = self.db.table(self.table).insert(data.model_dump()).execute()
        return result.data[0]

    def update(self, shop_id: str, data: ShopUpdate) -> dict:
        payload = {k: v for k, v in data.model_dump().items() if v is not None}
        result = self.db.table(self.table).update(payload).eq("id", shop_id).execute()
        return result.data[0]
