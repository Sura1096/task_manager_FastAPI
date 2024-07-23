from pydantic import BaseModel, ConfigDict


class TaskCreateSchema(BaseModel):
    title: str
    description: str
    status: bool | None = False


class TaskUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    task_id: int
    title: str
    description: str
    status: bool


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    task_id: int
    user_id: int
    title: str
    description: str
    status: bool
