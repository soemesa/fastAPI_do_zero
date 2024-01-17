import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import User
from src.schemas import UserSchema, UserPublic, UserList, UserDB

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", log_level="debug", port=8002, reload=True
    )


@app.get("/")
def read_root():
    return {"message": "Olá Mundo!"}


@app.post("/users/", response_model=UserPublic, status_code=201)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )
    if db_user:
        raise HTTPException(status_code=400, detail="Usuário já registrado")
    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get("/users/", response_model=UserList)
def read_users(
        skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User). offset(skip). limit(limit)).all()

    return {'users': users}


database = []


# @app.put("/users/{user_id}", response_model=UserPublic)
# def update_user(
#         user_id: int, user: UserSchema, session: Session = Depends(get_session)
# ):
#     db_user = session.scalar(select(User). where(User.id == user_id))
#
#     if not db_user:
#         raise HTTPException(status_code=404, detail="Usuário não encontrado")
#
#     db_user.username = user.username
#     db_user.password = user.password
#     db_user.email = user.email
#     session.commit()
#     session.refresh(db_user)
#
#     return db_user


@app.put("/users/{user_username}", response_model=UserPublic)
def update_user(
        user_username: str, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User). where(User.username == user_username))

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db_user.username = user.username
    db_user.password = user.password
    db_user.email = user.email
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete("/users/{user_id}", response_model=None)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail="User not found")

    del database[user_id - 1]

    return {"detail": "User deleted"}
