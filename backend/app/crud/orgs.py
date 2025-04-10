from uuid import UUID
from typing import Optional
from supabase import Client
from ..core.logging import logger
from ..core.database import get_supabase_client

async def create_organization(name: str, user_id: UUID) -> dict:
    """
    Create a new organization
    """
    supabase = get_supabase_client()
    
    # Insert the organization
    result = supabase.table("organizations").insert({
        "name": name,
        "created_by": str(user_id)
    }).execute()
    
    if not result.data:
        logger.error("Failed to create organization", user_id=user_id, name=name)
        raise Exception("Failed to create organization")
    
    return result.data[0]

async def get_organization(org_id: UUID) -> Optional[dict]:
    """
    Get organization by ID
    """
    supabase = get_supabase_client()
    
    result = supabase.table("organizations").select("*").eq("id", str(org_id)).execute()
    
    if not result.data:
        return None
    
    return result.data[0]

async def get_organization_by_user(user_id: UUID) -> Optional[dict]:
    """
    Get organization by user ID (through user_profiles)
    """
    supabase = get_supabase_client()
    
    # Get the user profile to find their organization
    # user_id is the same as the id in user_profiles table
    profile_result = supabase.table("user_profiles").select("org_id").eq("id", str(user_id)).execute()
    
    if not profile_result.data or not profile_result.data[0].get("org_id"):
        return None
    
    org_id = profile_result.data[0]["org_id"]
    
    # Then get the organization
    org_result = supabase.table("organizations").select("*").eq("id", org_id).execute()
    
    if not org_result.data:
        return None
    
    return org_result.data[0] 