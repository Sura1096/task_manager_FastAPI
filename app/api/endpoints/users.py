from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Any

from app.api.schemas.user import UserSchema, UserResponse
from app.core.security import get_token_by_username
from app.api.endpoints.users_methods import get_user_from_db, insert_user_db


auth_user_route = APIRouter(
    prefix='/auth'
)


@auth_user_route.post('/register/', response_model=Any[UserResponse | None, HTTPException])
async def register_user(user: UserSchema):
    user_in_db = await get_user_from_db(user.username)
    if not user_in_db:
        return await insert_user_db(user)
    else:
        raise HTTPException(status_code=409, detail='User with that username already exists.')


@auth_user_route.post('/login/')
async def login(user: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_in_db = await get_user_from_db(user.username)
    if not user_in_db or user_in_db.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    token = get_token_by_username(user.username)
    return token
