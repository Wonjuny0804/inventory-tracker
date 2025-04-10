from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID
from ...core.logging import logger
from ...schemas.orgs import OrganizationCreate, OrganizationResponse
from ...services.org_service import create_organization_with_admin
from ...core.database import get_supabase_client

router = APIRouter(prefix="/orgs", tags=["organizations"])

# OAuth2 scheme for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper to verify and get user from token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    supabase = get_supabase_client()
    try:
        # Verify the token and get user data
        result = supabase.auth.get_user(token)
        if not result.user:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return result.user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid authentication: {str(e)}")

@router.post("/", response_model=OrganizationResponse)
async def create_organization(
    org_data: OrganizationCreate,
    current_user = Depends(get_current_user)
):
    """
    Create a new organization and assign the current user as admin
    """
    try:
        user_id = UUID(current_user.id)
        logger.info("Creating organization", user_id=user_id, org_data=org_data.model_dump)
        org = await create_organization_with_admin(org_data.name, user_id)
        return org
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create organization: {str(e)}")

@router.get("/me", response_model=OrganizationResponse)
async def get_my_organization(current_user = Depends(get_current_user)):
    """
    Get the organization of the current user
    """
    from ...crud.orgs import get_organization_by_user
    
    try:
        user_id = UUID(current_user.id)
        org = await get_organization_by_user(user_id)
        if not org:
            logger.error("No organization found for current user", user_id=user_id)
            raise HTTPException(status_code=404, detail="No organization found for current user")
        logger.info("Organization found for current user", org=org)
        return org
    except HTTPException as http_exception:
        logger.warning("HTTPException in get_my_organization", user_id=user_id, details=str(http_exception))
        raise
    except Exception as e:
        logger.error("Unexpected error in get_my_organization", user_id=user_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to get organization: {str(e)}") 