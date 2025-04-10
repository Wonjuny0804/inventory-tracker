from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserProfileBase(BaseModel):
    """Base model for user profile"""
    email: Optional[str] = None
    role: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    """Model for creating a user profile"""
    org_id: Optional[UUID] = None

class UserProfileUpdate(UserProfileBase):
    """Model for updating a user profile"""
    org_id: Optional[UUID] = None

class UserProfileInDB(UserProfileBase):
    """Model for user profile in DB"""
    id: UUID
    org_id: Optional[UUID] = None
    created_at: Optional[datetime] = None

class UserProfileResponse(UserProfileBase):
    id: UUID
    org_id: Optional[UUID] = None
    role: Optional[str] = None
    created_at: datetime 