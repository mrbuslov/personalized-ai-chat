from fastapi import APIRouter, HTTPException, status, Depends, Query
from uuid import UUID
from typing import Optional

from schemas.chat import ChatCreate, ChatResponse, ChatUpdate, ChatListResponse, ChatWithMessagesResponse
from schemas.message import MessageListResponse, MessageResponse
from services.chat_service import chat_service
from services.message_service import message_service
from api.dependencies import get_current_user, verify_user_chat_access
from models import User

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_data: ChatCreate,
    current_user: User = Depends(get_current_user)
):
    """Create new chat"""
    chat = await chat_service.create_chat(current_user.id, chat_data)
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create chat"
        )
    
    return ChatResponse.from_orm(chat)


@router.get("/", response_model=ChatListResponse)
async def get_user_chats(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """Get all chats for current user"""
    result = await chat_service.get_chats_by_user(current_user.id, page, page_size)
    
    return ChatListResponse(
        chats=[ChatResponse.from_orm(chat) for chat in result["records"]],
        total_count=result["total_count"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"]
    )


@router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: UUID,
    current_user: User = Depends(verify_user_chat_access)
):
    """Get specific chat"""
    chat = await chat_service.get_chat_by_id(chat_id)
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    return ChatResponse.from_orm(chat)


@router.get("/{chat_id}/with-messages", response_model=ChatWithMessagesResponse)
async def get_chat_with_messages(
    chat_id: UUID,
    current_user: User = Depends(verify_user_chat_access)
):
    """Get chat with all messages"""
    chat = await chat_service.get_chat_with_messages(chat_id)
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    return ChatWithMessagesResponse.from_orm(chat)


@router.put("/{chat_id}", response_model=ChatResponse)
async def update_chat(
    chat_id: UUID,
    chat_data: ChatUpdate,
    current_user: User = Depends(verify_user_chat_access)
):
    """Update chat"""
    chat = await chat_service.update_chat(chat_id, chat_data)
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    return ChatResponse.from_orm(chat)


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat_id: UUID,
    current_user: User = Depends(verify_user_chat_access)
):
    """Delete chat"""
    success = await chat_service.delete_chat(chat_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )


@router.get("/{chat_id}/messages", response_model=MessageListResponse)
async def get_chat_messages(
    chat_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    current_user: User = Depends(verify_user_chat_access)
):
    """Get all messages for a chat"""
    result = await message_service.get_messages_by_chat(chat_id, page, page_size)
    
    return MessageListResponse(
        messages=[MessageResponse.from_orm(msg) for msg in result["records"]],
        total_count=result["total_count"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"]
    )