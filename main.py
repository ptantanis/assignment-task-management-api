from fastapi import FastAPI
from task import router
from task.database import engine


app = FastAPI()

app.include_router(router.router, tags=["tasks"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
