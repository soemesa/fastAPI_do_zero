from pydantic import BaseModel, ConfigDict

from src.models import TodoState


class UserSchema(BaseModel):
    username: str
    email: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class UserDB(UserSchema):
    id: int


class Message(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublic(BaseModel):
    id: int
    title: str
    description: str
    state: TodoState


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: str | None = None
