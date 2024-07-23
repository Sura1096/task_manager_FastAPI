from pydantic import BaseModel, constr, ConfigDict


class UserSchema(BaseModel):
    username: str
    password: constr(min_length=8, max_length=16)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    username: str
    password: str
