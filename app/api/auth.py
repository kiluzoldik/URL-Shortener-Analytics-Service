from fastapi import APIRouter


auth_router = APIRouter(prefix="/auth", tags=["Авторизация/Аутентификация"])


@auth_router.post("/signup")
async def registration():
    ...
    
    
@auth_router.post("/login")
async def login():
    ...
    
    
@auth_router.post("/refresh")
async def refresh_token():
    ...