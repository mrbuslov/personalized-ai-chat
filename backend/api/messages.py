from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID

from schemas.message import (
    MessageCreate, MessageResponse, MessageUpdate, 
    AIMessageGenerationRequest, AIMessageRevisionRequest,
    MessageImportRequest
)
from services.message_service import message_service
from api.dependencies import get_current_user, verify_user_chat_access, verify_user_message_access
from models import User

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new message (client message)"""
    # Verify user has access to the chat
    from services.chat_service import chat_service
    has_access = await chat_service.check_user_chat_access(current_user.id, message_data.chat_id)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this chat"
        )
    
    message = await message_service.create_message(message_data)
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create message"
        )
    
    return MessageResponse.from_orm(message)


@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: UUID,
    current_user: User = Depends(verify_user_message_access)
):
    """Get specific message"""
    message = await message_service.get_message_by_id(message_id)
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    return MessageResponse.from_orm(message)


@router.put("/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: UUID,
    message_data: MessageUpdate,
    current_user: User = Depends(verify_user_message_access)
):
    """Update message"""
    message = await message_service.update_message(message_id, message_data)
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )
    
    return MessageResponse.from_orm(message)


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: UUID,
    current_user: User = Depends(verify_user_message_access)
):
    """Delete message"""
    success = await message_service.delete_message(message_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )


@router.post("/generate-ai-response", response_model=MessageResponse)
async def generate_ai_response(
    request: AIMessageGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate AI response for a chat"""
    # Verify user has access to the chat
    from services.chat_service import chat_service
    has_access = await chat_service.check_user_chat_access(current_user.id, request.chat_id)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this chat"
        )
    
    message = await message_service.generate_ai_response(
        request.chat_id, 
        request.context_messages_count or 10
    )
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate AI response"
        )
    
    return MessageResponse.from_orm(message)


@router.post("/revise-with-ai", response_model=MessageResponse)
async def revise_message_with_ai(
    request: AIMessageRevisionRequest,
    current_user: User = Depends(verify_user_message_access)
):
    """Revise message using AI with specific instructions"""
    message = await message_service.revise_message_with_ai(
        request.message_id,
        request.revision_instructions
    )
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revise message with AI"
        )
    
    return MessageResponse.from_orm(message)


@router.post("/import", response_model=list[MessageResponse])
async def import_messages(
    request: MessageImportRequest,
    current_user: User = Depends(get_current_user)
):
    """Import multiple messages to a chat"""
    # Verify user has access to the chat
    from services.chat_service import chat_service
    has_access = await chat_service.check_user_chat_access(current_user.id, request.chat_id)
    if not has_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this chat"
        )
    
    messages = await message_service.import_messages(request.chat_id, request.messages)
    
    return [MessageResponse.from_orm(msg) for msg in messages]