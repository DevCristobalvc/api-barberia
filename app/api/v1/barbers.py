from fastapi import APIRouter, HTTPException
from app.database.supabase import get_client
from app.repositories.barber_repo import BarberRepository
from app.schemas.barber import BarberCreate, BarberUpdate

router = APIRouter(prefix="/barbers", tags=["barbers"])


@router.get("/{shop_id}")
async def list_barbers(shop_id: str, active_only: bool = True):
    db = get_client()
    repo = BarberRepository(db)
    return repo.list_by_shop(shop_id, active_only)


@router.get("/{shop_id}/{barber_id}")
async def get_barber(shop_id: str, barber_id: str):
    db = get_client()
    repo = BarberRepository(db)
    barber = repo.get_by_id(barber_id)
    if not barber or barber["shop_id"] != shop_id:
        raise HTTPException(status_code=404, detail="Barbero no encontrado")
    return barber


@router.post("/")
async def create_barber(data: BarberCreate):
    db = get_client()
    repo = BarberRepository(db)
    return repo.create(data)


@router.patch("/{barber_id}")
async def update_barber(barber_id: str, data: BarberUpdate):
    db = get_client()
    repo = BarberRepository(db)
    return repo.update(barber_id, data)


@router.get("/{barber_id}/schedule")
async def get_schedule(barber_id: str):
    db = get_client()
    repo = BarberRepository(db)
    return repo.get_schedule(barber_id)
