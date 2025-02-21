import json
from redis.asyncio import Redis  # Импортируем асинхронный Redis
from settings import redis_host, redis_port, redis_db, redis_live_time

class RedisCli:
    def __init__(
            self,
            redis_client: Redis = Redis(host=redis_host, port=redis_port, db=redis_db)
        ):
        self.redis_client = redis_client
        self.live_time = redis_live_time

    async def rd_create_obj(self, key, value,live_time=None):
        """Создаёт объект в Redis."""
        value = json.dumps(value)
        ttl = live_time if live_time is not None else self.live_time
        await self.redis_client.setex(key, ttl, value)

    async def rd_get_obj(self, key: str) -> dict | None:
        """Получает объект из Redis."""
        data = await self.redis_client.get(key)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data
        return None