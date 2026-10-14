from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        project_id: int,
        title: str,
        description: str,
        priority: int,
    ) -> Task:
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            priority=priority,
        )
        self.db.add(task)
        self.db.flush()
        return task

    def get_by_id(self, task_id: int) -> Task | None:
        return self.db.get(Task, task_id)

    def list_by_project(
        self,
        project_id: int,
        completed: bool | None,
        skip: int,
        limit: int,
    ) -> list[Task]:
        statement = select(Task).where(
            Task.project_id == project_id
        )

        if completed is not None:
            statement = statement.where(
                Task.completed == completed
            )

        statement = (
            statement
            .order_by(Task.id)
            .offset(skip)
            .limit(limit)
        )

        return list(self.db.scalars(statement).all())

    def update(self, task: Task) -> Task:
        self.db.flush()
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.flush()