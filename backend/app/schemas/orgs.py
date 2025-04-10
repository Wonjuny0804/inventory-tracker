from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class OrganizationResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    created_by: UUID 