from fastapi import Depends

from app.api.schemas.task import TaskCreateSchema, TaskResponse, TaskUpdateSchema
from app.services.task_manager_service import TasksService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork


async def get_task_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> TasksService:
    return TasksService(uow)


async def get_task_db(
        task_id: int,
        task_service: TasksService = Depends(get_task_service)
) -> TaskResponse | None:
    return await task_service.get_task(task_id)


async def insert_task_db(
        user_id: int,
        data: TaskCreateSchema,
        task_service: TasksService = Depends(get_task_service)
) -> TaskResponse | None:
    return await task_service.insert_task(user_id, data)


async def update_task_db(
        user_id: int,
        data: TaskUpdateSchema,
        task_service: TasksService = Depends(get_task_service)
) -> TaskResponse | None:
    return await task_service.update_task(user_id, data)


async def delete_task_db(
        task_id: int,
        task_service: TasksService = Depends(get_task_service)
) -> None:
    return await task_service.delete_task(task_id)
