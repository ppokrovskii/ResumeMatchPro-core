from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, Field, ConfigDict

class JobDescriptionDb(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    title: str
    company: str
    location: Optional[str] = None
    description: str
    requirements: list[str]
    skills: list[str]
    experience_level: Optional[str] = None
    salary_range: Optional[str] = None
    employment_type: Optional[str] = None
    created_at: str
    updated_at: str
    is_active: bool = True
    metadata: Optional[dict] = None
