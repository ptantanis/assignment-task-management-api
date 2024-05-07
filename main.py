from fastapi import FastAPI
from task import models, router
from database.database import engine

# Change to use migration file for real development.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router.router, tags=["tasks"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
