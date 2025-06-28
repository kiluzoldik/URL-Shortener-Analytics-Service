from app.utils.db_manager import DBManager
from app.utils.redis_manager import RedisManager


class BaseService:
    db: DBManager | None
    redis: RedisManager | None
    
    def __init__(
        self, 
        db: DBManager | None = None,
        redis: RedisManager | None = None
    ) -> None:
        self.db = db
        self.redis = redis