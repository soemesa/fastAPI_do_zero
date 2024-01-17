from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import User
from src.schemas import UserSchema, UserPublic, UserList, Message
from src.security import get_password_hash, get_current_user

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=UserPublic, status_code=201)
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


@router.get('/', response_model=UserList)
def read_users(
        skip: int = 0,
        limit: int = 100,
        session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return {'users': users}


@router.put("/{user_username}", response_model=UserPublic)
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


@router.delete("/{user_username}", response_model=Message)
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
