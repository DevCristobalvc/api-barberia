from langchain_core.tools import tool
from app.database.supabase import get_client
from app.repositories.shop_repo import ShopRepository
from app.repositories.barber_repo import BarberRepository


@tool
def get_shop_information(shop_id: str) -> dict:
    """
    Obtiene la información general de la barbería.
    Args:
        shop_id: ID de la barbería
    """
    db = get_client()
    shop_repo = ShopRepository(db)
    return shop_repo.get_by_id(shop_id) or {}


@tool
def list_services(shop_id: str) -> list[dict]:
    """
    Lista todos los servicios disponibles de la barbería.
    Args:
        shop_id: ID de la barbería
    """
    db = get_client()
    result = db.table("services").select("*").eq("shop_id", shop_id).eq("active", True).order("name").execute()
    return result.data or []


@tool
def list_barbers(shop_id: str) -> list[dict]:
    """
    Lista los barberos activos de la barbería.
    Args:
        shop_id: ID de la barbería
    """
    db = get_client()
    repo = BarberRepository(db)
    return repo.list_by_shop(shop_id)


@tool
def block_schedule(barber_id: str, start_datetime: str, end_datetime: str, reason: str | None = None) -> dict:
    """
    Bloquea un período en el horario de un barbero (vacaciones, descanso, etc.).
    Args:
        barber_id: ID del barbero
        start_datetime: inicio del bloqueo en ISO format
        end_datetime: fin del bloqueo en ISO format
        reason: motivo del bloqueo
    """
    db = get_client()
    result = db.table("blocked_slots").insert({
        "barber_id": barber_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "reason": reason,
    }).execute()
    return {"success": True, "blocked_slot_id": result.data[0]["id"]}


@tool
def unblock_schedule(blocked_slot_id: str) -> dict:
    """
    Elimina un bloqueo de horario.
    Args:
        blocked_slot_id: ID del bloqueo a eliminar
    """
    db = get_client()
    db.table("blocked_slots").delete().eq("id", blocked_slot_id).execute()
    return {"success": True}
