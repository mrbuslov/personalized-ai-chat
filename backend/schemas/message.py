from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from models.message import MessageRole


class MessageBase(BaseModel):
    content: str
    role: MessageRole


class MessageCreate(MessageBase):
    chat_id: UUID


class MessageUpdate(BaseModel):
    content: Optional[str] = None


class MessageResponse(MessageBase):
    id: UUID
    chat_id: UUID
    is_ai_generated: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    messages: List[MessageResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int


class AIMessageGenerationRequest(BaseModel):
    chat_id: UUID
    context_messages_count: Optional[int] = 10


class AIMessageRevisionRequest(BaseModel):
    message_id: UUID
    revision_instructions: str


class MessageImportRequest(BaseModel):
    chat_id: UUID
    messages: List[dict]