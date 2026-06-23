from fastapi import APIRouter
from app.api.v1 import appointments, clients, barbers, webhook

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(webhook.router)
api_router.include_router(appointments.router)
api_router.include_router(clients.router)
api_router.include_router(barbers.router)
