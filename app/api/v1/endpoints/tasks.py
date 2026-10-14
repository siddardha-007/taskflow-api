from fastapi import APIRouter, HTTPException, Query, Response, status

from app.api.deps import DbSession
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task import TaskService

router = APIRouter(
    prefix="/projects/{project_id}/tasks",
    tags=["Tasks"],
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    project_id: int,
    data: TaskCreate,
    db: DbSession,
):
    try:
        return TaskService(db).create_task(project_id, data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    project_id: int,
    db: DbSession,
    completed: bool | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
):
    try:
        return TaskService(db).list_tasks(
            project_id, completed, skip, limit
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(project_id: int, task_id: int, db: DbSession):
    try:
        return TaskService(db).get_task(project_id, task_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    project_id: int,
    task_id: int,
    data: TaskUpdate,
    db: DbSession,
):
    try:
        return TaskService(db).update_task(project_id, task_id, data)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(project_id: int, task_id: int, db: DbSession):
    try:
        TaskService(db).delete_task(project_id, task_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc