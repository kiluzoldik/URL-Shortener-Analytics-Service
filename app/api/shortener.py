from fastapi import APIRouter, Request

from app.api.dependencies import UserIdDep, DBDep
from app.schemas.links import AddRequestLink
from app.services.shortener import ShortenerService


short_router = APIRouter(prefix="/api/shortener", tags=["Укорачивание ссылки"])


@short_router.get("/health")
async def check_service(user_id: UserIdDep, request: Request):
    return await request.app


@short_router.post("/shorten")
async def create_short_link(db: DBDep, user_id: UserIdDep, data: AddRequestLink):
    try:
        return await ShortenerService(db).create_short_link(user_id, data)
    except Exception:
        raise Exception # исключение


@short_router.get("/links")
async def get_all_user_links():
    try:
        ...
    except Exception:
        raise Exception # исключение


@short_router.get("/links/active")
async def get_active_user_links():
    try:
        ...
    except Exception:
        raise Exception # исключение
    
    
@short_router.get("/links/inactive")
async def get_inactive_user_links():
    try:
        ...
    except Exception:
        raise Exception # исключение
    
    
@short_router.get("/links/{code}")
async def get_user_link(code: str):
    try:
        ...
    except Exception:
        raise Exception # исключение
    
    
@short_router.delete("/links/{code}")
async def delete_user_link(code: str):
    try:
        ...
    except Exception:
        raise Exception # исключение