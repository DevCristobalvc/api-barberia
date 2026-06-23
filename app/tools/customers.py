from langchain_core.tools import tool
from app.database.supabase import get_client
from app.repositories.customer_repo import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate


@tool
def search_customer(shop_id: str, phone: str) -> dict | None:
    """
    Busca un cliente por teléfono.
    Args:
        shop_id: ID de la barbería
        phone: número de teléfono del cliente
    Returns:
        datos del cliente o None si no existe
    """
    db = get_client()
    repo = CustomerRepository(db)
    return repo.get_by_phone(shop_id, phone)


@tool
def create_customer(shop_id: str, name: str, phone: str, notes: str | None = None) -> dict:
    """
    Crea un nuevo cliente.
    Args:
        shop_id: ID de la barbería
        name: nombre completo del cliente
        phone: número de teléfono
        notes: notas opcionales sobre el cliente
    """
    db = get_client()
    repo = CustomerRepository(db)
    data = CustomerCreate(shop_id=shop_id, name=name, phone=phone, notes=notes)
    return repo.create(data)


@tool
def update_customer(customer_id: str, name: str | None = None, notes: str | None = None) -> dict:
    """
    Actualiza datos de un cliente.
    Args:
        customer_id: ID del cliente
        name: nuevo nombre (opcional)
        notes: nuevas notas (opcional)
    """
    db = get_client()
    repo = CustomerRepository(db)
    data = CustomerUpdate(name=name, notes=notes)
    return repo.update(customer_id, data)
