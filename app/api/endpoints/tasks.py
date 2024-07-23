from fastapi import APIRouter, Depends, HTTPException, status

from typing import Any

from app.api.schemas.task import TaskCreateSchema, TaskUpdateSchema, TaskResponse
from app.core.security import get_user_from_token
from app.api.endpoints.tasks_methods import get_task_db, insert_task_db, update_task_db, delete_task_db
from app.api.endpoints.users_methods import get_user_from_db


tasks_route = APIRouter(
    prefix='/tasks'
)


@tasks_route.get(
    '/{task_id}',
    response_model=Any[TaskResponse | None, HTTPException]
)
async def get_task_by_id(
        task_id: int,
        cur_user: str = Depends(get_user_from_token)
):
    user = await get_user_from_db(cur_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    else:
        return await get_task_db(task_id)


@tasks_route.post(
    '/add_task',
    response_model=Any[TaskResponse | None, HTTPException]
)
async def add_task(
        data: TaskCreateSchema,
        cur_user: str = Depends(get_user_from_token)
):
    user = await get_user_from_db(cur_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    else:
        return await insert_task_db(user.user_id, data)


@tasks_route.put(
    '/update_task',
    response_model=Any[TaskResponse | None, HTTPException]
)
async def update_task(
        data: TaskUpdateSchema,
        cur_user: str = Depends(get_user_from_token)
):
    user = await get_user_from_db(cur_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    else:
        return await update_task_db(user.user_id, data)


@tasks_route.delete('/{task_id}', response_model=Any[None, HTTPException])
async def remove_task(task_id: int, cur_user: str = Depends(get_user_from_token)):
    user = await get_user_from_db(cur_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    else:
        return await delete_task_db(task_id)
