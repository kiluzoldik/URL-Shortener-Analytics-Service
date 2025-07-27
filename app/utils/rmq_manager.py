from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection, AbstractChannel

from app.config.config import settings


class RMQManager:
    def __init__(self):
        self._connection: AbstractRobustConnection | None = None
        self._channel: AbstractChannel | None = None

    @staticmethod
    async def get_connection() -> AbstractRobustConnection:
        return await connect_robust(settings.RMQ_URL)

    @property
    def channel(self) -> AbstractRobustConnection:
        if self._channel is None:
            raise Exception("Error in context manager rmq")
        return self._channel

    async def __aenter__(self):
        self._connection = await self.get_connection()
        self._channel = await self._connection.channel()
        return self

    async def __aexit__(self, *args):
        if self._channel.is_open:
            await self._channel.close()
        if self._connection.is_open:
            await self._connection.close()
