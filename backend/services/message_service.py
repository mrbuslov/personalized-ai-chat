from typing import Optional, List, Dict, Any
from uuid import UUID

from common.database import db
from models import Message, Chat
from models.message import MessageRole
from schemas.message import MessageCreate, MessageUpdate
from services.ai_service import ai_service


class MessageService:
    async def create_message(self, message_data: MessageCreate) -> Optional[Message]:
        """Create a new message"""
        # Verify chat exists
        chat = await db.get_record_by_id(Chat, message_data.chat_id)
        if not chat:
            return None
        
        return await db.create_record(Message, **message_data.dict())
    
    async def create_ai_message(self, chat_id: UUID, content: str) -> Optional[Message]:
        """Create an AI-generated manager message"""
        return await db.create_record(
            Message,
            content=content,
            role=MessageRole.MANAGER,
            is_ai_generated=True,
            chat_id=chat_id
        )
    
    async def get_message_by_id(self, message_id: UUID) -> Optional[Message]:
        """Get message by ID"""
        return await db.get_record_by_id(Message, message_id)
    
    async def get_messages_by_chat(
        self, 
        chat_id: UUID, 
        page: int = 1, 
        page_size: int = 50
    ) -> Dict[str, Any]:
        """Get all messages for a chat with pagination"""
        return await db.get_records_paginated(
            Message,
            page=page,
            page_size=page_size,
            order_by="created_at",
            chat_id=chat_id
        )
    
    async def update_message(self, message_id: UUID, message_data: MessageUpdate) -> Optional[Message]:
        """Update message"""
        update_data = {k: v for k, v in message_data.dict().items() if v is not None}
        if not update_data:
            return await self.get_message_by_id(message_id)
        
        success = await db.update_record(Message, message_id, **update_data)
        if success:
            return await self.get_message_by_id(message_id)
        return None
    
    async def delete_message(self, message_id: UUID) -> bool:
        """Delete message"""
        return await db.delete_record(Message, message_id)
    
    async def generate_ai_response(self, chat_id: UUID, context_count: int = 10) -> Optional[Message]:
        """Generate AI response for a chat"""
        # Generate AI response content
        ai_content = await ai_service.generate_manager_response(chat_id, context_count)
        if not ai_content:
            return None
        
        # Create AI message
        return await self.create_ai_message(chat_id, ai_content)
    
    async def revise_message_with_ai(
        self, 
        message_id: UUID, 
        revision_instructions: str
    ) -> Optional[Message]:
        """Revise existing message using AI"""
        # Get original message
        original_message = await self.get_message_by_id(message_id)
        if not original_message:
            return None
        
        # Generate revised content
        revised_content = await ai_service.revise_message_with_ai(message_id, revision_instructions)
        if not revised_content:
            return None
        
        # Update message with revised content
        return await self.update_message(message_id, MessageUpdate(content=revised_content))
    
    async def import_messages(self, chat_id: UUID, messages_data: List[dict]) -> List[Message]:
        """Import multiple messages to a chat"""
        imported_messages = []
        
        for msg_data in messages_data:
            try:
                # Validate required fields
                if "content" not in msg_data or "role" not in msg_data:
                    continue
                
                # Ensure role is valid
                if msg_data["role"] not in [MessageRole.CLIENT, MessageRole.MANAGER]:
                    continue
                
                message = await db.create_record(
                    Message,
                    content=msg_data["content"],
                    role=MessageRole(msg_data["role"]),
                    is_ai_generated=msg_data.get("is_ai_generated", False),
                    chat_id=chat_id
                )
                
                if message:
                    imported_messages.append(message)
                    
            except Exception as e:
                print(f"Error importing message: {e}")
                continue
        
        return imported_messages
    
    async def check_message_chat_access(self, message_id: UUID, chat_id: UUID) -> bool:
        """Check if message belongs to the specified chat"""
        message = await self.get_message_by_id(message_id)
        return message is not None and message.chat_id == chat_id
    
    async def get_recent_messages(self, chat_id: UUID, limit: int = 10) -> List[Message]:
        """Get recent messages for a chat"""
        messages = await db.get_records(Message, chat_id=chat_id)
        return messages[-limit:] if len(messages) > limit else messages


message_service = MessageService()