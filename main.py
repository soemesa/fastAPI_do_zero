import uvicorn
from fastapi import FastAPI

from src.routes import users, auth, todos

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", log_level="debug", port=8002, reload=True
    )


@app.get("/")
def read_root():
    return {"message": "Olá Mundo!"}



