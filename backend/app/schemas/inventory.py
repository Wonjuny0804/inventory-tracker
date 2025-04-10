from pydantic import BaseModel
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime

# Create Schema
class InventoryItemCreate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[int] = 1
    location: Optional[str] = None
    status: Optional[Literal["available", "in_use", "reserved", "missing"]] = "available"

# Update Schema
class InventoryItemUpdate(BaseModel):
    name: Optional[str]
    quantity: Optional[int]
    location: Optional[str]
    status: Optional[Literal["available", "in_use", "reserved", "missing"]]

# Response Schema
class InventoryItemResponse(BaseModel):
    id: UUID
    org_id: UUID
    name: str
    quantity: int
    location: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
