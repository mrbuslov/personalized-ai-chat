from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer

from schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest, UserRegistration
from schemas.user import UserResponse
from services.auth_service import auth_service
from api.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


# Registration endpoint removed - only admins can create users


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest):
    """Login user and return JWT tokens"""
    tokens = await auth_service.login(login_data.email, login_data.password)
    
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_data: RefreshTokenRequest):
    """Refresh access token using refresh token"""
    tokens = await auth_service.refresh_access_token(refresh_data.refresh_token)
    
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    return tokens


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse.from_orm(current_user)


@router.post("/logout")
async def logout():
    """Logout user (client should discard tokens)"""
    return {"message": "Successfully logged out"}