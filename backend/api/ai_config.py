from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID
from typing import Optional

from schemas.ai_configuration import AIConfigurationCreate, AIConfigurationResponse, AIConfigurationUpdate
from services.ai_service import ai_service
from api.dependencies import get_current_user, verify_user_chat_access
from models import User, AIConfiguration
from common.database import db

router = APIRouter(prefix="/ai-config", tags=["ai-configuration"])


@router.post("/", response_model=AIConfigurationResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_configuration(
    config_data: AIConfigurationCreate,
    current_user: User = Depends(get_current_user)
):
    """Create AI configuration (global or chat-specific)"""
    # If chat_id is provided, verify access
    if config_data.chat_id:
        from services.chat_service import chat_service
        has_access = await chat_service.check_user_chat_access(current_user.id, config_data.chat_id)
        if not has_access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this chat"
            )
    
    config_dict = config_data.dict()
    config_dict["company_id"] = current_user.company_id
    
    config = await db.create_record(AIConfiguration, **config_dict)
    
    return AIConfigurationResponse.from_orm(config)


@router.get("/global", response_model=Optional[AIConfigurationResponse])
async def get_global_ai_configuration(
    current_user: User = Depends(get_current_user)
):
    """Get global AI configuration for user's company"""
    config = await db.get_record_by_field(
        AIConfiguration,
        company_id=current_user.company_id,
        chat_id=None
    )
    
    if not config:
        return None
    
    return AIConfigurationResponse.from_orm(config)


@router.get("/chat/{chat_id}", response_model=Optional[AIConfigurationResponse])
async def get_chat_ai_configuration(
    chat_id: UUID,
    current_user: User = Depends(verify_user_chat_access)
):
    """Get AI configuration for specific chat"""
    config = await db.get_record_by_field(
        AIConfiguration,
        company_id=current_user.company_id,
        chat_id=chat_id
    )
    
    if not config:
        return None
    
    return AIConfigurationResponse.from_orm(config)


@router.put("/global", response_model=AIConfigurationResponse)
async def update_global_ai_configuration(
    config_data: AIConfigurationUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update global AI configuration"""
    # Get or create global configuration
    config = await db.get_record_by_field(
        AIConfiguration,
        company_id=current_user.company_id,
        chat_id=None
    )
    
    if not config:
        # Create new global configuration
        config = await db.create_record(
            AIConfiguration,
            company_id=current_user.company_id,
            chat_id=None,
            global_prompt=config_data.global_prompt
        )
    else:
        # Update existing configuration
        update_data = {k: v for k, v in config_data.dict().items() if v is not None}
        await db.update_record(AIConfiguration, config.id, **update_data)
        config = await db.get_record_by_id(AIConfiguration, config.id)
    
    return AIConfigurationResponse.from_orm(config)


@router.put("/chat/{chat_id}", response_model=AIConfigurationResponse)
async def update_chat_ai_configuration(
    chat_id: UUID,
    config_data: AIConfigurationUpdate,
    current_user: User = Depends(verify_user_chat_access)
):
    """Update AI configuration for specific chat"""
    # Get or create chat-specific configuration
    config = await db.get_record_by_field(
        AIConfiguration,
        company_id=current_user.company_id,
        chat_id=chat_id
    )
    
    if not config:
        # Create new chat-specific configuration
        config = await db.create_record(
            AIConfiguration,
            company_id=current_user.company_id,
            chat_id=chat_id,
            global_prompt=config_data.global_prompt
        )
    else:
        # Update existing configuration
        update_data = {k: v for k, v in config_data.dict().items() if v is not None}
        await db.update_record(AIConfiguration, config.id, **update_data)
        config = await db.get_record_by_id(AIConfiguration, config.id)
    
    return AIConfigurationResponse.from_orm(config)


@router.delete("/global", status_code=status.HTTP_204_NO_CONTENT)
async def delete_global_ai_configuration(
    current_user: User = Depends(get_current_user)
):
    """Delete global AI configuration"""
    await db.delete_records(
        AIConfiguration,
        company_id=current_user.company_id,
        chat_id=None
    )


@router.delete("/chat/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_ai_configuration(
    chat_id: UUID,
    current_user: User = Depends(verify_user_chat_access)
):
    """Delete AI configuration for specific chat"""
    await db.delete_records(
        AIConfiguration,
        company_id=current_user.company_id,
        chat_id=chat_id
    )