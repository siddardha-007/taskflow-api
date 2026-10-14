from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    description: str = Field(default="", max_length=1000)

    # Temporary until Phase 4 derives ownership from JWT.
    owner_id: int = Field(gt=0)


class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
    )


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)