import aio_pika

from app.config.config import settings
from app.utils.rmq_manager import RMQManager


class BaseConsumer:
    def __init__(self):
        self.queue_name = settings.MQ_ROUTING_KEY


class BaseProducer:
    pass


class BaseProcessMessage:
    pass
