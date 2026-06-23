from fastapi import APIRouter, HTTPException
from app.database.supabase import get_client
from app.schemas.service import ServiceCreate, ServiceUpdate

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/{shop_id}")
async def list_services(shop_id: str, active_only: bool = True):
    db = get_client()
    query = db.table("services").select("*").eq("shop_id", shop_id)
    if active_only:
        query = query.eq("active", True)
    result = query.order("name").execute()
    return result.data or []


@router.post("/")
async def create_service(data: ServiceCreate):
    db = get_client()
    result = db.table("services").insert(data.model_dump()).execute()
    return result.data[0]


@router.patch("/{service_id}")
async def update_service(service_id: str, data: ServiceUpdate):
    db = get_client()
    payload = {k: v for k, v in data.model_dump().items() if v is not None}
    result = db.table("services").update(payload).eq("id", service_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return result.data[0]


@router.delete("/{service_id}")
async def delete_service(service_id: str):
    db = get_client()
    db.table("services").update({"active": False}).eq("id", service_id).execute()
    return {"success": True}
