from sqlalchemy.orm import Session

from app.models.task import Task
from app.repositories.project import ProjectRepository
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.tasks = TaskRepository(db)
        self.projects = ProjectRepository(db)

    def create_task(
        self,
        project_id: int,
        data: TaskCreate,
    ) -> Task:
        if self.projects.get_by_id(project_id) is None:
            raise LookupError("Project not found")

        try:
            task = self.tasks.create(
                project_id=project_id,
                title=data.title,
                description=data.description,
                priority=data.priority,
            )

            self.db.commit()
            self.db.refresh(task)
            return task

        except Exception:
            self.db.rollback()
            raise

    def list_tasks(
        self,
        project_id: int,
        completed: bool | None,
        skip: int,
        limit: int,
    ) -> list[Task]:
        if self.projects.get_by_id(project_id) is None:
            raise LookupError("Project not found")

        return self.tasks.list_by_project(
            project_id=project_id,
            completed=completed,
            skip=skip,
            limit=limit,
        )

    def get_task(self, project_id: int, task_id: int) -> Task:
        task = self.tasks.get_by_id(task_id)

        if task is None or task.project_id != project_id:
            raise LookupError("Task not found in this project")

        return task

    def update_task(
        self,
        project_id: int,
        task_id: int,
        data: TaskUpdate,
    ) -> Task:
        task = self.get_task(project_id, task_id)
        updates = data.model_dump(exclude_unset=True)

        if not updates:
            raise ValueError("Provide at least one field to update")

        if any(value is None for value in updates.values()):
            raise ValueError("Updated fields cannot be null")

        try:
            for field, value in updates.items():
                setattr(task, field, value)

            self.tasks.update(task)
            self.db.commit()
            self.db.refresh(task)
            return task

        except Exception:
            self.db.rollback()
            raise

    def delete_task(self, project_id: int, task_id: int) -> None:
        task = self.get_task(project_id, task_id)

        try:
            self.tasks.delete(task)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise