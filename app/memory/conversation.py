import json
import logging
import redis.asyncio as aioredis
from app.config.settings import settings

logger = logging.getLogger(__name__)
TTL = 60 * 60 * 6  # 6 hours


class ConversationMemory:
    def __init__(self):
        self._redis: aioredis.Redis | None = None
        self._available: bool = True
        # In-process fallback when Redis is unavailable
        self._local: dict[str, dict] = {}

    async def _get_redis(self) -> aioredis.Redis | None:
        if not self._available:
            return None
        try:
            if self._redis is None:
                self._redis = await aioredis.from_url(
                    settings.redis_url, decode_responses=True, socket_connect_timeout=2
                )
            await self._redis.ping()
            return self._redis
        except Exception as e:
            logger.warning("Redis no disponible, usando memoria local: %s", e)
            self._available = False
            self._redis = None
            return None

    def _key(self, shop_id: str, phone: str) -> str:
        return f"conversation:{shop_id}:{phone}"

    async def get(self, shop_id: str, phone: str) -> dict:
        r = await self._get_redis()
        if r:
            try:
                raw = await r.get(self._key(shop_id, phone))
                if raw:
                    return json.loads(raw)
            except Exception:
                pass
        # Fallback a memoria local
        return self._local.get(self._key(shop_id, phone), {"messages": [], "customer": None, "context": {}})

    async def save(self, shop_id: str, phone: str, state: dict) -> None:
        r = await self._get_redis()
        if r:
            try:
                await r.setex(self._key(shop_id, phone), TTL, json.dumps(state))
                return
            except Exception:
                pass
        self._local[self._key(shop_id, phone)] = state

    async def append_message(self, shop_id: str, phone: str, role: str, content: str) -> None:
        state = await self.get(shop_id, phone)
        state["messages"].append({"role": role, "content": content})
        if len(state["messages"]) > 30:
            state["messages"] = state["messages"][-30:]
        await self.save(shop_id, phone, state)

    async def clear(self, shop_id: str, phone: str) -> None:
        r = await self._get_redis()
        if r:
            try:
                await r.delete(self._key(shop_id, phone))
                return
            except Exception:
                pass
        self._local.pop(self._key(shop_id, phone), None)


memory = ConversationMemory()
