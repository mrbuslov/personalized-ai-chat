from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from uuid import UUID

from models import User
from services.auth_service import auth_service
from services.user_service import user_service

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """Get current authenticated user"""
    token = credentials.credentials
    user = await auth_service.get_current_user(token)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    """Get current user if authenticated, None otherwise"""
    if not credentials:
        return None
    
    token = credentials.credentials
    return await auth_service.get_current_user(token)


def require_company_access(user: User = Depends(get_current_user)):
    """Dependency to ensure user has company access"""
    return user


async def verify_user_chat_access(chat_id: UUID, user: User = Depends(get_current_user)) -> User:
    """Verify user has access to specific chat"""
    from services.chat_service import chat_service
    
    has_access = await chat_service.check_user_chat_access(user.id, chat_id)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this chat"
        )
    
    return user


async def verify_user_message_access(message_id: UUID, user: User = Depends(get_current_user)) -> User:
    """Verify user has access to specific message"""
    from services.message_service import message_service
    from services.chat_service import chat_service
    
    message = await message_service.get_message_by_id(message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    # Check if user has access to the chat containing this message
    has_access = await chat_service.check_user_chat_access(user.id, message.chat_id)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this message"
        )
    
    return user