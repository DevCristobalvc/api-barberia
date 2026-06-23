from fastapi import APIRouter, HTTPException
from app.database.supabase import get_client
from app.schemas.shop import ShopCreate, ShopUpdate

router = APIRouter(prefix="/shops", tags=["shops"])


@router.get("/{shop_id}")
async def get_shop(shop_id: str):
    db = get_client()
    result = db.table("shops").select("*").eq("id", shop_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Barbería no encontrada")
    return result.data


@router.patch("/{shop_id}")
async def update_shop(shop_id: str, data: ShopUpdate):
    db = get_client()
    payload = {k: v for k, v in data.model_dump().items() if v is not None}
    result = db.table("shops").update(payload).eq("id", shop_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Barbería no encontrada")
    return result.data[0]
