from abc import ABC, abstractmethod

from sqlalchemy import select, update, insert, delete
from sqlalchemy.sql import and_
from sqlalchemy.ext.asyncio import AsyncSession


class UsersAbstractRepo(ABC):
    @abstractmethod
    async def get_user_db(self, username: str):
        raise NotImplementedError

    @abstractmethod
    async def insert_user_db(self, data: dict):
        raise NotImplementedError


class TasksAbstractRepo(ABC):
    @abstractmethod
    async def get_task_db(self, task_id: int):
        raise NotImplementedError

    @abstractmethod
    async def insert_task_db(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def update_task_db(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_task_db(self, task_id: int):
        raise NotImplementedError


class UsersRepo(UsersAbstractRepo):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_db(self, username: str):
        stmt = select(self.model).where(self.model.username == username)
        user = await self.session.execute(stmt)
        result = user.scalar_one_or_none()
        if result:
            return result
        return None

    async def insert_user_db(self, data: dict):
        stmt = insert(self.model).values(**data)
        await self.session.execute(stmt)
        return await self.get_user_db(data["username"])


class TasksRepo(TasksAbstractRepo):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_task_db(self, task_id: int):
        stmt = select(self.model).where(self.model.task_id == task_id)
        task = await self.session.execute(stmt)
        result = task.scalar_one_or_none()
        if result:
            return result
        return None

    async def insert_task_db(self, data: dict):
        stmt = insert(self.model).values(**data)
        await self.session.execute(stmt)

    async def update_task_db(self, data: dict):
        stmt = update(self.model).where(and_(
                self.model.task_id == data["task_id"],
                self.model.user_id == data["user_id"]
        )).values(
            title=data["title"],
            description=data["description"],
            status=data["status"]
        )
        await self.session.execute(stmt)

    async def delete_task_db(self, task_id: int):
        stmt = delete(self.model).where(self.model.task_id == task_id)
        await self.session.execute(stmt)
