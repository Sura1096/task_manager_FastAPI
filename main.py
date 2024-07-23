import uvicorn
from fastapi import FastAPI

from app.api.endpoints.tasks import tasks_route
from app.api.endpoints.users import auth_user_route


app = FastAPI()

app.include_router(auth_user_route)
app.include_router(tasks_route)


if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)
