from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="TaskFlow API",
    description="API for managing tasks and workflows built while learning FastAPI",
    version="1.0.0"
)

class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100, description="The title of the task")
    description: str = Field(default="", max_length=500, description="A detailed description of the task")
    priority: int = Field(default=1, ge=1, le=5, description="Priority of the task (1-5)")

tasks = []
next_task_id = 1

@app.get("/")
def home():
    return {"message": "Welcome to the TaskFlow API!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    global next_task_id

    new_task = {
        "id": next_task_id,
        **task.model_dump(),
        "completed": False,
    }

    tasks.append(new_task)
    next_task_id += 1

    return new_task

@app.get("/tasks")
def get_tasks(
    completed: bool | None = None,
    skip: int = 0,
    limit: int = 10,
):
    result = tasks

    if completed is not None:
        result = [
            task for task in result
            if task["completed"] == completed
        ]

    return result[skip:skip + limit]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found",
    )