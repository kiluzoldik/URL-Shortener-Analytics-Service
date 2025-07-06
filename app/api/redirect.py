from fastapi import APIRouter

from app.api.dependencies import DBDep, RedisDep, UserIdDep
from app.services.shortener import ShortenerService


redirect_router = APIRouter(prefix="", tags=["Редирект на исходную ссылку"])

@redirect_router.get("/{code}", summary="Перенаправление на исходную ссылку")
async def redirect(code: str, redis: RedisDep, db: DBDep):
    try:
        return await ShortenerService(db, redis).redirect(code)
    except Exception:
        raise Exception # исключение