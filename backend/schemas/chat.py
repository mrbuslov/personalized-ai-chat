from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from .user import UserResponse
from .message import MessageResponse


class ChatBase(BaseModel):
    name: str
    client_description: Optional[str] = None
    special_instructions: Optional[str] = None


class ChatCreate(ChatBase):
    pass


class ChatUpdate(BaseModel):
    name: Optional[str] = None
    client_description: Optional[str] = None
    special_instructions: Optional[str] = None


class ChatResponse(ChatBase):
    id: UUID
    user_id: UUID
    company_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ChatWithMessagesResponse(ChatResponse):
    messages: List[MessageResponse] = []


class ChatListResponse(BaseModel):
    chats: List[ChatResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int