from uuid import UUID
from typing import Optional, Dict, Any
from ..core.database import get_supabase_client

async def get_user_profile(user_id: UUID) -> Optional[dict]:
    """
    Get a user profile by user ID
    """
    supabase = get_supabase_client()
    
    result = supabase.table("user_profiles").select("*").eq("id", str(user_id)).execute()
    
    if not result.data:
        return None
    
    return result.data[0]

async def create_user_profile(user_data: Dict[str, Any]) -> dict:
    """
    Create a new user profile
    """
    supabase = get_supabase_client()
    
    result = supabase.table("user_profiles").insert(user_data).execute()
    
    if not result.data:
        raise Exception("Failed to create user profile")
    
    return result.data[0]

async def update_user_profile(profile_id: UUID, update_data: Dict[str, Any]) -> dict:
    """
    Update an existing user profile
    """
    supabase = get_supabase_client()
    
    result = supabase.table("user_profiles").update(update_data).eq("id", str(profile_id)).execute()
    
    if not result.data:
        raise Exception("Failed to update user profile")
    
    return result.data[0]

# This function is redundant with get_user_profile since 
# in our DB structure id and user_id are the same
async def update_user_profile_by_user_id(user_id: UUID, update_data: Dict[str, Any]) -> dict:
    """
    Update an existing user profile by user_id (same as profile id)
    """
    return await update_user_profile(user_id, update_data)

async def get_user_auth_data(user_id: UUID) -> Optional[dict]:
    """
    Get user auth data from Supabase auth
    """
    supabase = get_supabase_client()
    
    # This is using the admin API to get user data
    result = supabase.auth.admin.get_user_by_id(str(user_id))
    
    if not result.user:
        return None
    
    return result.user 