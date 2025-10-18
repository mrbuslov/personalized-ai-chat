from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Optional, Dict, Any
from uuid import UUID

from common.database import db
from common.settings import settings
from models import User, Company
from schemas.auth import TokenResponse


class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Generate password hash"""
        return self.pwd_context.hash(password)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password"""
        user = await db.get_record_by_field(User, email=email)
        if not user or not self.verify_password(password, user.password_hash):
            return None
        return user
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            return payload
        except JWTError:
            return None
    
    async def get_current_user(self, token: str) -> Optional[User]:
        """Get current user from JWT token"""
        payload = self.verify_token(token)
        if payload is None:
            return None
            
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
            
        user = await db.get_record_by_id(User, UUID(user_id))
        return user
    
    async def login(self, email: str, password: str) -> Optional[TokenResponse]:
        """Login user and return tokens"""
        user = await self.authenticate_user(email, password)
        if not user:
            return None
            
        access_token = self.create_access_token(data={"sub": str(user.id)})
        refresh_token = self.create_refresh_token(data={"sub": str(user.id)})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )
    
    async def refresh_access_token(self, refresh_token: str) -> Optional[TokenResponse]:
        """Refresh access token using refresh token"""
        payload = self.verify_token(refresh_token)
        if payload is None:
            return None
            
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
            
        user = await db.get_record_by_id(User, UUID(user_id))
        if not user:
            return None
            
        access_token = self.create_access_token(data={"sub": str(user.id)})
        new_refresh_token = self.create_refresh_token(data={"sub": str(user.id)})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60
        )
    
    async def register_user(self, email: str, password: str, name: str, company_name: str) -> Optional[User]:
        """Register new user with company"""
        existing_user = await db.get_record_by_field(User, email=email)
        if existing_user:
            return None
            
        # Create company first
        company = await db.create_record(Company, name=company_name)
        
        # Create user
        password_hash = self.get_password_hash(password)
        user = await db.create_record(
            User,
            email=email,
            password_hash=password_hash,
            name=name,
            company_id=company.id
        )
        
        return user


auth_service = AuthService()