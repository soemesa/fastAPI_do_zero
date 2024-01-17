import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import User
from src.schemas import UserSchema, UserPublic, UserList, Message, Token
from src.security import get_password_hash, verify_password, create_access_token, get_current_user

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

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username, email=user.email, password=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get("/users/", response_model=UserList)
def read_users(
        skip: int = 0,
        limit: int = 100,
        session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return {'users': users}


@app.put("/users/{user_username}", response_model=UserPublic)
def update_user(
        user_username: str,
        user: UserSchema,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    if current_user.username != user_username:
        raise HTTPException(status_code=404, detail="Permissões insuficientes")

    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete("/users/{user_username}", response_model=Message)
def delete_user(
        user_username: str,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    if current_user != user_username:
        raise HTTPException(status_code=404, detail="Permissões insuficientes")

    session.delete(current_user)
    session.commit()

    return {"detail": "Usuário deletado com sucesso"}


@app.post('/token', response_model=Token)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)
):
    user = session.scalar(select(User).where(User.username == form_data.username))

    if not user:
        raise HTTPException(
            status_code=400, detail='Usuário inválido'
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400, detail='Senha inválida'
        )
    access_token = create_access_token(data={'sub': user.username})

    return Token(access_token=access_token, token_type='bearer')
