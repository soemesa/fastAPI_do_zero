from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str
    password: str


class UserPublic(BaseModel):
    username: str
    email: str
