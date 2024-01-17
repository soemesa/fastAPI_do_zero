from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import User
from src.schemas import Token
from src.security import verify_password, create_access_token

router = APIRouter(prefix='/auth', tags=['auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Session = Annotated[Session, Depends(get_session)]


@router.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2Form, session: Session):
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
