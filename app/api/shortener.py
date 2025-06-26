from fastapi import APIRouter

from app.api.dependencies import UserIdDep, DBDep


short_router = APIRouter(prefix="/shortener", tags=["Укорачивание ссылки"])


@short_router.get("/health")
async def check_service(user_id: UserIdDep):
    return {"detail": user_id}


@short_router.post("/shorten")
async def create_short_link(url: str):
    return {"detail": f"link - {url}"}


@short_router.get("/links")
async def get_all_user_links():
    ...


@short_router.get("/links/active")
async def get_active_user_links():
    ...
    
    
@short_router.get("/links/inactive")
async def get_inactive_user_links():
    ...
    
    
@short_router.get("/links/{code}")
async def get_user_link(code: str):
    ...
    
    
@short_router.delete("/links/{code}")
async def delete_user_link(code: str):
    ...