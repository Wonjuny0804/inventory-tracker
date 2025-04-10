from uuid import UUID
from typing import Dict, Any, Optional
from ..crud import orgs, users
from ..core.logging import logger
from ..schemas.orgs import OrganizationCreate, OrganizationResponse
from ..schemas.users import UserProfileUpdate
from fastapi import HTTPException

async def create_organization_with_admin(name: str, user_id: UUID) -> Dict:
    """
    Create a new organization and set the creating user as admin
    """
    try:
        org = await orgs.create_organization(name, user_id)
        logger.info("Organization created", org=org)
    except Exception as e:
        logger.error("Failed to create organization", user_id=user_id, name=name, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to create organization: {str(e)}")
    

    user_profile = await users.get_user_profile(user_id)
    
    if not user_profile:
        # Create a user profile if it doesn't exist
        try:
            # Use a dictionary for user data
            user_data = {
                "id": str(user_id),
                "org_id": org["id"],
                "role": "admin"
            }
            await users.create_user_profile(user_data)
        except Exception as e:
            # If we fail to create the profile, we should probably clean up the org
            # but for simplicity we'll just raise an error
            raise HTTPException(status_code=500, detail=f"Failed to create user profile: {str(e)}")
    else:
        # Update the existing profile
        try:
            await users.update_user_profile(
                user_id,  # user_id is the same as the profile_id
                {
                    "org_id": org["id"],
                    "role": "admin"
                }
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update user profile: {str(e)}")
    
    return org 