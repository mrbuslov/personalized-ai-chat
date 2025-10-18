from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class AIConfigurationBase(BaseModel):
    global_prompt: Optional[str] = None


class AIConfigurationCreate(AIConfigurationBase):
    chat_id: Optional[UUID] = None


class AIConfigurationUpdate(BaseModel):
    global_prompt: Optional[str] = None


class AIConfigurationResponse(AIConfigurationBase):
    id: UUID
    company_id: UUID
    chat_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True