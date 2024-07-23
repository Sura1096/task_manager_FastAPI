from fastapi import Depends

from app.api.schemas.user import UserSchema, UserResponse
from app.services.task_manager_service import UsersService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork


async def get_users_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> UsersService:
    return UsersService(uow)


# Функция для получения пользовательских данных на основе имени пользователя
async def get_user_from_db(
        username: str,
        users_service: UsersService = Depends(get_users_service)
) -> UserResponse | None:
    return await users_service.get_user(username)


async def insert_user_db(
        data: UserSchema,
        users_service: UsersService = Depends(get_users_service)
) -> UserResponse | None:
    return await users_service.insert_user(data)
