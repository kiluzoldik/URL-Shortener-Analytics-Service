from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.api.dependencies import DBDep, RedisDep
from app.services.shortener import ShortenerService


redirect_router = APIRouter(prefix="", tags=["Редирект на исходную ссылку"])

@redirect_router.get("/{code}", summary="Перенаправление на исходную ссылку")
async def redirect(code: str, redis: RedisDep, db: DBDep):
    try:
        url = await ShortenerService(db, redis).url_for_redirect(code)
        return RedirectResponse(url=url)
    except Exception:
        raise Exception # исключение`11`