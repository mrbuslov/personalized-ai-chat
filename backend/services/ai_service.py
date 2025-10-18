import openai
import asyncio
from typing import List, Optional
from uuid import UUID

from common.database import db
from common.settings import settings
from models import Message, Chat, AIConfiguration
from models.message import MessageRole


class AIService:
    def __init__(self):
        self.openai_client = None
        self._init_clients()
    
    def _init_clients(self):
        """Initialize AI clients based on available API keys"""
        self.openai_client = openai
        self.openai_client.api_key = settings.openai_api_key
    
    async def get_ai_configuration(self, company_id: UUID, chat_id: Optional[UUID] = None) -> str:
        """Get AI configuration prompt (chat-specific or global)"""
        chat_config = None
        if chat_id:
            chat_config = await db.get_record_by_field(
                AIConfiguration, 
                company_id=company_id, 
                chat_id=chat_id
            )
        
        if chat_config and chat_config.global_prompt:
            return chat_config.global_prompt
        
        # Fall back to global configuration
        global_config = await db.get_record_by_field(
            AIConfiguration,
            company_id=company_id,
            chat_id=None
        )
        
        if global_config and global_config.global_prompt:
            return global_config.global_prompt
        
        # Default prompt
        return "You are a professional customer service manager. Respond helpfully and professionally to customer inquiries."
    
    async def build_conversation_context(self, chat_id: UUID, context_count: int = 10) -> List[dict]:
        """Build conversation context from recent messages"""
        messages = await db.get_records(
            Message,
            chat_id=chat_id
        )
        
        # Get the last N messages
        recent_messages = messages[-context_count:] if len(messages) > context_count else messages
        
        conversation = []
        for message in recent_messages:
            role = "user" if message.role == MessageRole.CLIENT else "assistant"
            conversation.append({
                "role": role,
                "content": message.content
            })
        
        return conversation
    
    async def generate_manager_response(
        self, 
        chat_id: UUID, 
        context_messages_count: int = 10
    ) -> Optional[str]:
        """Generate AI response as manager to client messages"""
        try:
            # Get chat details
            chat = await db.get_record_by_id(Chat, chat_id)
            if not chat:
                return None
            
            # Build system prompt
            ai_prompt = await self.get_ai_configuration(chat.company_id, chat_id)
            
            # Add client description if available
            if chat.client_description:
                ai_prompt += f"\n\nClient Description: {chat.client_description}"
            
            # Add special instructions if available
            if chat.special_instructions:
                ai_prompt += f"\n\nSpecial Instructions: {chat.special_instructions}"
            
            # Get conversation history
            conversation = await self.build_conversation_context(chat_id, context_messages_count)
            
            # Prepare messages for AI
            messages = [
                {"role": "system", "content": ai_prompt},
                *conversation
            ]
            
            if settings.default_ai_provider == "openai" and self.openai_client:
                return await self._generate_openai_response(messages)
            else:
                return "AI service not configured. Please set up OpenAI API key."
                
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return None
    
    async def _generate_openai_response(self, messages: List[dict]) -> Optional[str]:
        """Generate response using OpenAI"""
        try:
            response = await asyncio.to_thread(
                self.openai_client.ChatCompletion.create,
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None
    
    async def revise_message_with_ai(
        self, 
        message_id: UUID, 
        revision_instructions: str
    ) -> Optional[str]:
        """Revise existing message using AI with specific instructions"""
        try:
            message = await db.get_record_by_id(Message, message_id)
            if not message:
                return None
            
            # Get chat context
            chat = await db.get_record_by_id(Chat, message.chat_id)
            if not chat:
                return None
            
            # Build revision prompt
            system_prompt = f"""You are helping revise a customer service message. 
            
Original message: {message.content}

Revision instructions: {revision_instructions}

Please provide a revised version of the message that incorporates the requested changes while maintaining professionalism."""
            
            messages = [{"role": "system", "content": system_prompt}]
            
            if settings.default_ai_provider == "openai" and self.openai_client:
                return await self._generate_openai_response(messages)
            else:
                return "AI service not configured. Please set up OpenAI API key."
                
        except Exception as e:
            print(f"Error revising message with AI: {e}")
            return None


ai_service = AIService()
