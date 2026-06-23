from langchain_core.messages import HumanMessage, AIMessage
from app.agents.assistant import assistant_graph
from app.memory.conversation import memory
from app.database.supabase import get_client
from app.repositories.shop_repo import ShopRepository
from app.repositories.barber_repo import BarberRepository
from app.prompts.system_prompt import build_system_prompt


class AgentService:
    async def process_message(self, shop_id: str, phone: str, user_message: str) -> str:
        db = get_client()
        shop = ShopRepository(db).get_by_id(shop_id)
        if not shop:
            return "Lo siento, no pude encontrar la barbería. Por favor contacta directamente."

        barbers = BarberRepository(db).list_by_shop(shop_id)
        services_raw = db.table("services").select("*").eq("shop_id", shop_id).eq("active", True).execute()
        services = services_raw.data or []

        system_prompt = build_system_prompt(shop, barbers, services)

        state = await memory.get(shop_id, phone)
        history = [
            HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
            for m in state.get("messages", [])
        ]

        result = await assistant_graph.ainvoke({
            "messages": history + [HumanMessage(content=user_message)],
            "shop_id": shop_id,
            "phone": phone,
            "system_prompt": system_prompt,
        })

        last_message = result["messages"][-1]
        response_text = last_message.content if hasattr(last_message, "content") else str(last_message)

        await memory.append_message(shop_id, phone, "user", user_message)
        await memory.append_message(shop_id, phone, "assistant", response_text)

        return response_text


agent_service = AgentService()
