from fastapi import APIRouter

from app.api.dependencies import RedisDep, UserIdDep, DBDep
from app.schemas.links import AddRequestLink, Link
from app.services.shortener import ShortenerService


short_router = APIRouter(prefix="/api/shortener", tags=["Укорачивание ссылки"])


@short_router.get("/health")
async def check_service():
    return {"detail": "OK"}


@short_router.post("/shorten", summary="Сокращение ссылки")
async def create_short_link(db: DBDep, user_id: UserIdDep, redis: RedisDep, data: AddRequestLink) -> str:
    try:
        return await ShortenerService(db, redis).create_short_link(user_id, data)
    except Exception:
        raise Exception # исключение


@short_router.get("/links")
async def get_all_user_links(user_id: UserIdDep, db: DBDep, active: bool = True) -> list[Link]:
    try:
        return await ShortenerService(db).get_all_user_links(user_id, active)
    except Exception:
        raise Exception # исключение
    
    
@short_router.get("/links/{code}")
async def get_user_link(user_id: UserIdDep, db: DBDep, code: str):
    try:
        return await ShortenerService(db).get_user_link_by_code(user_id, code)
    except Exception:
        raise Exception # исключение
    
    
@short_router.delete("/links/{code}")
async def delete_user_link(user_id: UserIdDep, db: DBDep, redis: RedisDep, code: str):
    try:
        await ShortenerService(db, redis).delete_link(user_id, code)
    except Exception:
        raise Exception # исключение
    
    return {"detail": "Ссылка успешно удалена"}