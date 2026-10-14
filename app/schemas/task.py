
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(default="", max_length=500)
    priority: int = Field(default=1, ge=1, le=5)


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=500,
    )
    priority: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )
    completed: bool | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
