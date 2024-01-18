from enum import Enum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


class BaseModel(DeclarativeBase):
    pass


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(25), unique=True)
    email: Mapped[str] = mapped_column(String(80), unique=True)
    password: Mapped[str] = mapped_column(nullable=True)

    todos: Mapped[list['Todo']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )


class Todo(BaseModel):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    state: Mapped[TodoState] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped[User] = relationship(back_populates='todos')
