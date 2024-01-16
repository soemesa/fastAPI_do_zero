import uvicorn
from fastapi import FastAPI

from src.schemas import UserSchema, UserPublic

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', log_level='debug', port=8002, reload=True)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=201, response_model=UserPublic)
def create_user(user: UserSchema):
    return user
