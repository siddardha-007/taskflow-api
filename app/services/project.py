from sqlalchemy.orm import Session

from app.models.project import Project
from app.repositories.project import ProjectRepository
from app.repositories.user import UserRepository
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, db: Session):
        self.db = db
        self.projects = ProjectRepository(db)
        self.users = UserRepository(db)

    def create_project(self, data: ProjectCreate) -> Project:
        try:
            owner = self.users.get_by_id(data.owner_id)

            if owner is None:
                raise ValueError("User not found")

            project = self.projects.create(
                name=data.name,
                description=data.description,
                owner_id=data.owner_id,
            )

            self.db.commit()
            self.db.refresh(project)
            return project

        except Exception:
            self.db.rollback()
            raise

    def get_project(self, project_id: int) -> Project:
        project = self.projects.get_by_id(project_id)

        if project is None:
            raise LookupError("Project not found")

        return project

    def list_projects(self, owner_id: int) -> list[Project]:
        if self.users.get_by_id(owner_id) is None:
            raise LookupError("User not found")

        return self.projects.list_by_owner(owner_id)

    def update_project(
        self,
        project_id: int,
        data: ProjectUpdate,
    ) -> Project:
        project = self.get_project(project_id)
        updates = data.model_dump(exclude_unset=True)

        if not updates:
            raise ValueError("Provide at least one field to update")

        if any(value is None for value in updates.values()):
            raise ValueError("Updated fields cannot be null")

        try:
            for field, value in updates.items():
                setattr(project, field, value)

            self.projects.update(project)
            self.db.commit()
            self.db.refresh(project)
            return project

        except Exception:
            self.db.rollback()
            raise

    def delete_project(self, project_id: int) -> None:
        project = self.get_project(project_id)

        try:
            self.projects.delete(project)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise