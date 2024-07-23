from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    tasks = relationship('Tasks', back_populates='user')


class Tasks(Base):
    __tablename__ = 'tasks'

    task_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(index=True)
    status: Mapped[bool] = mapped_column(default=False)

    user = relationship('Users', back_populates='tasks')
