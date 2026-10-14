from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    def create_user(self, data: UserCreate) -> User:
        if self.users.get_by_email(str(data.email)):
            raise ValueError("Email is already registered")

        try:
            user = self.users.create(
                name=data.name,
                email=str(data.email),
            )
            self.db.commit()
            self.db.refresh(user)
            return user

        except IntegrityError as exc:
            self.db.rollback()
            raise ValueError("Email is already registered") from exc

        except Exception:
            self.db.rollback()
            raise

    def get_user(self, user_id: int) -> User:
        user = self.users.get_by_id(user_id)

        if user is None:
            raise LookupError("User not found")

        return user