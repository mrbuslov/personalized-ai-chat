from typing import Optional, List
from uuid import UUID

from common.database import db
from models import User
from schemas.user import UserCreate, UserUpdate
from services.auth_service import auth_service


class UserService:
    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        user_dict = user_data.dict()
        # Hash password before storing
        user_dict["password_hash"] = auth_service.get_password_hash(user_dict.pop("password"))
        return await db.create_record(User, **user_dict)
    
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        return await db.get_record_by_id(User, user_id)
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return await db.get_record_by_field(User, email=email)
    
    async def get_users_by_company(self, company_id: UUID) -> List[User]:
        """Get all users in a company"""
        return await db.get_records(User, company_id=company_id)
    
    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> Optional[User]:
        """Update user"""
        update_data = {k: v for k, v in user_data.dict().items() if v is not None}
        
        # Hash password if provided
        if "password" in update_data:
            update_data["password_hash"] = auth_service.get_password_hash(update_data.pop("password"))
        
        if not update_data:
            return await self.get_user_by_id(user_id)
        
        success = await db.update_record(User, user_id, **update_data)
        if success:
            return await self.get_user_by_id(user_id)
        return None
    
    async def delete_user(self, user_id: UUID) -> bool:
        """Delete user"""
        return await db.delete_record(User, user_id)
    
    async def check_user_company_access(self, user_id: UUID, company_id: UUID) -> bool:
        """Check if user belongs to the specified company"""
        user = await self.get_user_by_id(user_id)
        return user is not None and user.company_id == company_id


user_service = UserService()