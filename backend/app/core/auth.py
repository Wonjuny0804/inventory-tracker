from fastapi import HTTPException, status, Request, Depends
from typing import Optional
import logging
from ..core.database import get_supabase_client
from postgrest.exceptions import APIError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class User:
    def __init__(self, id: str, email: Optional[str] = None, org_id: Optional[str] = None):
        self.id = id
        self.email = email
        self.org_id = org_id

    def get(self, key: str):
        return getattr(self, key)

async def get_current_user(request: Request) -> User:
    """
    Authenticate user using Supabase's auth.getUser() method.
    Returns User object with data from Supabase Auth and user_profiles.
    """
    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Missing authentication token"
        )

    token = auth_header.replace("Bearer ", "").strip()
    
    # Get Supabase client
    supabase = get_supabase_client()
    
    try:
        # Use Supabase's built-in method to validate the JWT and get the user
        response = supabase.auth.get_user(token)
        print(response.user)
        
        # Extract user data from response
        user = response.user
        
        if not user or not user.id:
            logger.error("No user found with the provided token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid authentication token"
            )
        
        user_id = user.id
        email = user.email
        
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid authentication token"
        )
    
    # Fetch additional user data from user_profiles table
    try:
        profile_response = supabase.table("user_profiles").select("*").eq("id", user_id).single().execute()
        
        # If no profile exists yet, return basic user
        if not profile_response.data:
            logger.info(f"No profile found for user {user_id}, returning basic user")
            return User(id=user_id, email=email)
            
        # Return user with profile data
        return User(
            id=user_id, 
            email=email, 
            org_id=profile_response.data.get("org_id")
        )
    except APIError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching user data"
        )

def get_user_dependency():
    """
    Returns a dependency function for FastAPI routes
    """
    return Depends(get_current_user)
