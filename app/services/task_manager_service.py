from app.utils.unitofwork import IUnitOfWork

from app.api.schemas.task import TaskResponse, TaskCreateSchema, TaskUpdateSchema
from app.api.schemas.user import UserSchema, UserResponse


class UsersService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_user(self, username: str) -> UserResponse | None:
        async with self.uow:
            user = await self.uow.users.get_user_db(username)
            user_return = None
            if user:
                user_return = UserResponse.model_validate(user)
            await self.uow.commit()
            return user_return

    async def insert_user(self, data: UserSchema) -> UserResponse | None:
        data_dict: dict = data.model_dump()
        async with self.uow:
            user = await self.uow.users.insert_user_db(data_dict)
            user_return = None
            if user:
                user_return = UserResponse.model_validate(user)
            await self.uow.commit()
            return user_return


class TasksService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_task(self, task_id: int) -> TaskResponse | None:
        async with self.uow:
            task = await self.uow.tasks.get_task_db(task_id)
            task_return = None
            if task:
                task_return = TaskResponse.model_validate(task)
            await self.uow.commit()
            return task_return

    async def insert_task(self, user_id: int, data: TaskCreateSchema) -> TaskResponse | None:
        data_dict: dict = data.model_dump()
        data_dict["user_id"] = user_id
        async with self.uow:
            task = await self.uow.tasks.insert_task_db(data_dict)
            task_return = None
            if task_return:
                task_return = TaskResponse.model_validate(task)
            await self.uow.commit()
            return task_return

    async def update_task(self, user_id: int, data: TaskUpdateSchema) -> TaskResponse | None:
        data_dict: dict = data.model_dump()
        data_dict["user_id"] = user_id
        async with self.uow:
            task = await self.uow.tasks.update_task_db(data_dict)
            task_return = None
            if task_return:
                task_return = TaskResponse.model_validate(task)
            await self.uow.commit()
            return task_return

    async def delete_task(self, task_id: int) -> None:
        async with self.uow:
            task = await self.uow.tasks.delete_task_db(task_id)
            await self.uow.commit()
            return task
