from pydantic import BaseModel
from datetime import datetime


class IncomingMessage(BaseModel):
    shop_id: str
    phone: str
    message: str
    timestamp: datetime | None = None


class OutgoingMessage(BaseModel):
    phone: str
    message: str
    shop_id: str
