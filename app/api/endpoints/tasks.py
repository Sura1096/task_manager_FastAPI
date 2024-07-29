from fastapi import APIRouter, Depends, HTTPException, status

from app.api.endpoints.users import get_users_service
from app.api.schemas.task import TaskCreateSchema, TaskUpdateSchema, TaskResponse

from app.core.security import get_user_from_token

from app.services.task_manager_service import TasksService
from app.services.task_manager_service import UsersService

from app.utils.unitofwork import IUnitOfWork, UnitOfWork


tasks_route = APIRouter(
    prefix='/tasks'
)


async def get_task_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> TasksService:
    return TasksService(uow)


@tasks_route.get(
    '/get_task/{task_id}',
    response_model=TaskResponse
)
async def get_task_by_id(
        task_id: int,
        cur_user: str = Depends(get_user_from_token),
        users_service: UsersService = Depends(get_users_service),
        task_service: TasksService = Depends(get_task_service)
):
    user = await users_service.get_user(cur_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    else:
        task_return = await task_service.get_task(task_id)
        if task_return:
            return task_return
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found.'
            )


@tasks_route.post('/add_task')
async def add_task(
        data: TaskCreateSchema,
        cur_user: str = Depends(get_user_from_token),
        users_service: UsersService = Depends(get_users_service),
        task_service: TasksService = Depends(get_task_service)
):
    user = await users_service.get_user(cur_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    else:
        await task_service.insert_task(user.user_id, data)
        return {'message': 'Task successfully added.'}


@tasks_route.put(
    '/update_task',
    response_model=TaskResponse
)
async def update_task(
        data: TaskUpdateSchema,
        cur_user: str = Depends(get_user_from_token),
        users_service: UsersService = Depends(get_users_service),
        task_service: TasksService = Depends(get_task_service)
):
    user = await users_service.get_user(cur_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    else:
        task_exists = await task_service.get_task(data.task_id)
        if task_exists:
            await task_service.update_task(user.user_id, data)
            return await task_service.get_task(data.task_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found.'
            )


@tasks_route.delete('/delete_task/{task_id}')
async def remove_task(
        task_id: int, cur_user: str = Depends(get_user_from_token),
        users_service: UsersService = Depends(get_users_service),
        task_service: TasksService = Depends(get_task_service)
):
    user = await users_service.get_user(cur_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    else:
        task_exists = await task_service.get_task(task_id)
        if task_exists:
            await task_service.delete_task(task_id)
            return {'message': 'Task successfully deleted.'}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task not found.'
            )
