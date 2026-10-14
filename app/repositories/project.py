from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        name: str,
        description: str,
        owner_id: int,
    ) -> Project:
        project = Project(
            name=name,
            description=description,
            owner_id=owner_id,
        )
        self.db.add(project)
        self.db.flush()
        return project

    def get_by_id(self, project_id: int) -> Project | None:
        return self.db.get(Project, project_id)

    def list_by_owner(self, owner_id: int) -> list[Project]:
        statement = (
            select(Project)
            .where(Project.owner_id == owner_id)
            .order_by(Project.id)
        )
        return list(self.db.scalars(statement).all())

    def update(self, project: Project) -> Project:
        self.db.flush()
        return project

    def delete(self, project: Project) -> None:
        self.db.delete(project)
        self.db.flush()