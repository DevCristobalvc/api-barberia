from fastapi import APIRouter, HTTPException
from app.database.supabase import get_client
from app.repositories.customer_repo import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("/{shop_id}")
async def list_clients(shop_id: str, q: str | None = None):
    db = get_client()
    repo = CustomerRepository(db)
    if q:
        return repo.search(shop_id, q)
    return repo.list_by_shop(shop_id)


@router.get("/{shop_id}/{customer_id}")
async def get_client_by_id(shop_id: str, customer_id: str):
    db = get_client()
    repo = CustomerRepository(db)
    customer = repo.get_by_id(customer_id)
    if not customer or customer["shop_id"] != shop_id:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return customer


@router.post("/")
async def create_customer(data: CustomerCreate):
    db = get_client()
    repo = CustomerRepository(db)
    return repo.create(data)


@router.patch("/{customer_id}")
async def update_customer(customer_id: str, data: CustomerUpdate):
    db = get_client()
    repo = CustomerRepository(db)
    return repo.update(customer_id, data)
