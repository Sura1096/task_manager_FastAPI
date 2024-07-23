from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta, UTC

from app.core.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login/')

# Секретный ключ для подписи и верификации токенов JWT
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM

# Переменные для установки срока действия токена
TIME_NOW = datetime.now(UTC)
TOKEN_EXP_MIN = 60


# Функция для создания JWT токена
def create_jwt_token(data: dict):
    payload = data.copy()
    expiration_time = TIME_NOW + timedelta(minutes=TOKEN_EXP_MIN)

    payload.update({'iat': TIME_NOW, 'exp': expiration_time})

    token = jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm=ALGORITHM)
    return token


def get_token_by_username(username: str):
    try:
        return {"access_token": create_jwt_token({
            "sub": username,
            })}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Функция получения User'а по токену
def get_user_from_token(token=Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM])
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Access Token has expired or expiration date is invalid!',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={'WWW-Authenticate': 'Bearer'},
        )
