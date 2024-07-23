from app.db.models import Users, Tasks
from app.repositories.base_repo import UsersRepo, TasksRepo


class UsersRepository(UsersRepo):
    model = Users


class TasksRepository(TasksRepo):
    model = Tasks
