from taskiq_aio_pika import AioPikaBroker

from app.config.config import settings


broker = AioPikaBroker(url=settings.RMQ_URL)
