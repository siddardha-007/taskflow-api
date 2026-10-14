from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


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

    @model_validator(mode="after")
    def validate_not_empty(self):
        if not self.model_fields_set:
            raise ValueError("Provide at least one field to update")
        return self


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    completed: bool
    created_at: datetime
    project_id: int | None

    model_config = ConfigDict(from_attributes=True)