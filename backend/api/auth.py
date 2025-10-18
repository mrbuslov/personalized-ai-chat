from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer

from schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest, UserRegistration
from schemas.user import UserResponse
from services.auth_service import auth_service
from api.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegistration):
    """Register new user with company"""
    user = await auth_service.register_user(
        email=user_data.email,
        password=user_data.password,
        name=user_data.name,
        company_name=user_data.company_name
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    return UserResponse.from_orm(user)


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