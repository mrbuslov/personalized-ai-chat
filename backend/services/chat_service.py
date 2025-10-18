from typing import Optional, List, Dict, Any
from uuid import UUID

from common.database import db
from models import Chat, User
from schemas.chat import ChatCreate, ChatUpdate


class ChatService:
    async def create_chat(self, user_id: UUID, chat_data: ChatCreate) -> Optional[Chat]:
        """Create a new chat"""
        # Get user to get company_id
        user = await db.get_record_by_id(User, user_id)
        if not user:
            return None
        
        chat_dict = chat_data.dict()
        chat_dict.update({
            "user_id": user_id,
            "company_id": user.company_id
        })
        
        return await db.create_record(Chat, **chat_dict)
    
    async def get_chat_by_id(self, chat_id: UUID) -> Optional[Chat]:
        """Get chat by ID"""
        return await db.get_record_by_id(Chat, chat_id)
    
    async def get_chats_by_user(self, user_id: UUID, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """Get all chats for a user with pagination"""
        return await db.get_records_paginated(
            Chat,
            page=page,
            page_size=page_size,
            order_by="-created_at",
            user_id=user_id
        )
    
    async def get_chats_by_company(self, company_id: UUID, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """Get all chats for a company with pagination"""
        return await db.get_records_paginated(
            Chat,
            page=page,
            page_size=page_size,
            order_by="-created_at",
            company_id=company_id
        )
    
    async def update_chat(self, chat_id: UUID, chat_data: ChatUpdate) -> Optional[Chat]:
        """Update chat"""
        update_data = {k: v for k, v in chat_data.dict().items() if v is not None}
        if not update_data:
            return await self.get_chat_by_id(chat_id)
        
        success = await db.update_record(Chat, chat_id, **update_data)
        if success:
            return await self.get_chat_by_id(chat_id)
        return None
    
    async def delete_chat(self, chat_id: UUID) -> bool:
        """Delete chat and all its messages"""
        return await db.delete_record(Chat, chat_id)
    
    async def check_user_chat_access(self, user_id: UUID, chat_id: UUID) -> bool:
        """Check if user has access to the chat"""
        chat = await self.get_chat_by_id(chat_id)
        return chat is not None and chat.user_id == user_id
    
    async def check_company_chat_access(self, company_id: UUID, chat_id: UUID) -> bool:
        """Check if chat belongs to the company"""
        chat = await self.get_chat_by_id(chat_id)
        return chat is not None and chat.company_id == company_id
    
    async def get_chat_with_messages(self, chat_id: UUID) -> Optional[Chat]:
        """Get chat with all its messages"""
        chats = await db.get_records_with_relations(Chat, ["messages"], id=chat_id)
        return chats[0] if chats else None


chat_service = ChatService()