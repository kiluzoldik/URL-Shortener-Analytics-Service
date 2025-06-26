from fastapi import APIRouter, Response

from app.schemas.auth import AddUser
from app.services.auth import AuthService
from app.api.dependencies import DBDep, UserIdDep


auth_router = APIRouter(prefix="/auth", tags=["Авторизация/Аутентификация"])


@auth_router.post("/signup", summary="Регистрация пользователя")
async def registration(db: DBDep, data: AddUser):
    try:
        await AuthService(db).registration(data)
    except Exception:
        raise Exception # исключение
    
    return {"detail": "Успешная регистрация"}
    
    
@auth_router.post("/login", summary="Аутентификация пользователя")
async def login(db: DBDep, response: Response, data: AddUser):
    try:
        token = await AuthService(db).login_user(response, data)
    except:
        raise Exception # исключение
    
    return {"access_token": token}

@auth_router.get("/me", summary="Информация о пользователе")
async def get_me(db: DBDep, user_id: UserIdDep):
    try:
        return await AuthService(db).user_info(user_id)
    except Exception:
        raise Exception # исключение
    
@auth_router.post("/logout", summary="Выход из системы")
async def logout(response: Response):
    try:
        await AuthService().logout_user(response)
    except Exception:
        raise Exception # исключение
    
    return {"detail": "Вы успешно вышли из системы"}