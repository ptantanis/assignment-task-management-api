from uuid import UUID
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/tasks", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task=task)


@app.patch("/tasks/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: UUID, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)
):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    new_version = schemas.Task.model_validate(db_task).model_copy(
        update=task_update.model_dump(exclude_unset=True)
    )
    new_version.version += 1

    return crud.update_task(db, task=new_version)


@app.post("/tasks/{task_id}/undo", response_model=schemas.Task)
def undo_task(task_id: UUID, db: Session = Depends(get_db)):
    return crud.undo_task(db, task_id=task_id)


@app.get("/tasks/{task_id}", response_model=schemas.Task)
def get_task(task_id: UUID, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.get("/tasks", response_model=list[schemas.Task])
def search_tasks(
    task_filter: schemas.TaskFilter = Depends(), db: Session = Depends(get_db)
):
    users = crud.search_tasks(db, task_filter=task_filter)
    return users
