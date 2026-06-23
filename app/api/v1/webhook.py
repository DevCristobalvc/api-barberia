from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.schemas.message import IncomingMessage, OutgoingMessage
from app.services.agent_service import agent_service

router = APIRouter(prefix="/webhook", tags=["webhook"])


async def process_and_reply(msg: IncomingMessage):
    try:
        response = await agent_service.process_message(
            shop_id=msg.shop_id,
            phone=msg.phone,
            user_message=msg.message,
        )
        print(f"[{msg.shop_id}] {msg.phone}: {msg.message}")
        print(f"[{msg.shop_id}] SofIA: {response}")
    except Exception as e:
        print(f"Error processing message: {e}")


@router.post("/message")
async def receive_message(msg: IncomingMessage, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_and_reply, msg)
    return {"status": "received"}


@router.post("/message/sync")
async def receive_message_sync(msg: IncomingMessage) -> dict:
    """Procesa el mensaje y devuelve la respuesta de forma síncrona (para testing)."""
    try:
        response = await agent_service.process_message(
            shop_id=msg.shop_id,
            phone=msg.phone,
            user_message=msg.message,
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
