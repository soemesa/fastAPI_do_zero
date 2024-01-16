import uvicorn
from fastapi import FastAPI

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', log_level='debug', port=8002, reload=True)


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}