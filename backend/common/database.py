from tortoise import Tortoise, connections
from tortoise.transactions import in_transaction
from typing import Optional, Dict, Any, List
from uuid import UUID

from .settings import settings


class DatabaseFacade:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def init_db(self):
        """Initialize database connection and generate schemas"""
        await Tortoise.init(
            db_url=settings.db.database_url,
            modules={"models": ["models"]},
        )
        await Tortoise.generate_schemas()
    
    async def close_db(self):
        """Close database connections"""
        await connections.close_all()
    
    async def create_record(self, model_class, **data) -> Any:
        """Create a new record in the database"""
        return await model_class.create(**data)
    
    async def get_record_by_id(self, model_class, record_id: UUID) -> Optional[Any]:
        """Get a record by its ID"""
        return await model_class.get_or_none(id=record_id)
    
    async def get_record_by_field(self, model_class, **filters) -> Optional[Any]:
        """Get a single record by field filters"""
        return await model_class.get_or_none(**filters)
    
    async def get_records(self, model_class, **filters) -> List[Any]:
        """Get multiple records with optional filters"""
        queryset = model_class.all()
        if filters:
            queryset = queryset.filter(**filters)
        return await queryset
    
    async def get_records_with_relations(self, model_class, relations: List[str], **filters) -> List[Any]:
        """Get records with prefetched relations"""
        queryset = model_class.all().prefetch_related(*relations)
        if filters:
            queryset = queryset.filter(**filters)
        return await queryset
    
    async def update_record(self, model_class, record_id: UUID, **data) -> bool:
        """Update a record by ID, returns True if updated"""
        updated_count = await model_class.filter(id=record_id).update(**data)
        return updated_count > 0
    
    async def update_record_instance(self, instance, **data) -> Any:
        """Update an existing model instance"""
        for key, value in data.items():
            setattr(instance, key, value)
        await instance.save()
        return instance
    
    async def delete_record(self, model_class, record_id: UUID) -> bool:
        """Delete a record by ID, returns True if deleted"""
        deleted_count = await model_class.filter(id=record_id).delete()
        return deleted_count > 0
    
    async def delete_records(self, model_class, **filters) -> int:
        """Delete multiple records, returns count of deleted records"""
        return await model_class.filter(**filters).delete()
    
    async def count_records(self, model_class, **filters) -> int:
        """Count records with optional filters"""
        queryset = model_class.all()
        if filters:
            queryset = queryset.filter(**filters)
        return await queryset.count()
    
    async def execute_transaction(self, operations: List[callable]) -> Any:
        """Execute multiple operations in a transaction"""
        async with in_transaction() as connection:
            results = []
            for operation in operations:
                result = await operation(connection)
                results.append(result)
            return results
    
    async def get_records_paginated(
        self, 
        model_class, 
        page: int = 1, 
        page_size: int = 20, 
        order_by: Optional[str] = None,
        **filters
    ) -> Dict[str, Any]:
        """Get paginated records"""
        offset = (page - 1) * page_size
        
        queryset = model_class.all()
        if filters:
            queryset = queryset.filter(**filters)
        
        if order_by:
            queryset = queryset.order_by(order_by)
        
        total_count = await queryset.count()
        records = await queryset.offset(offset).limit(page_size)
        
        return {
            "records": records,
            "total_count": total_count,
            "page": page,
            "page_size": page_size,
            "total_pages": (total_count + page_size - 1) // page_size
        }


# Global database instance
db = DatabaseFacade()
