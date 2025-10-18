from typing import Optional, List
from uuid import UUID

from common.database import db
from models import Company
from schemas.company import CompanyCreate, CompanyUpdate


class CompanyService:
    async def create_company(self, company_data: CompanyCreate) -> Company:
        """Create a new company"""
        return await db.create_record(Company, **company_data.dict())
    
    async def get_company_by_id(self, company_id: UUID) -> Optional[Company]:
        """Get company by ID"""
        return await db.get_record_by_id(Company, company_id)
    
    async def get_companies(self) -> List[Company]:
        """Get all companies"""
        return await db.get_records(Company)
    
    async def update_company(self, company_id: UUID, company_data: CompanyUpdate) -> Optional[Company]:
        """Update company"""
        # Filter out None values
        update_data = {k: v for k, v in company_data.dict().items() if v is not None}
        if not update_data:
            return await self.get_company_by_id(company_id)
        
        success = await db.update_record(Company, company_id, **update_data)
        if success:
            return await self.get_company_by_id(company_id)
        return None
    
    async def delete_company(self, company_id: UUID) -> bool:
        """Delete company"""
        return await db.delete_record(Company, company_id)


company_service = CompanyService()