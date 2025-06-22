from fastapi import APIRouter


short_router = APIRouter(prefix="/shorter", tags=["Укорачивание ссылки"])


@short_router.post("")
async def create_short_link(url: str):
    return {"detail": f"link - {url}"}