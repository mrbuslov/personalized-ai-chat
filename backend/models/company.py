from tortoise.models import Model
from tortoise import fields
import uuid


class Company(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    # Reverse relations
    users = fields.ReverseRelation["User"]
    chats = fields.ReverseRelation["Chat"]
    ai_configurations = fields.ReverseRelation["AIConfiguration"]
    
    class Meta:
        table = "companies"
        
    def __str__(self):
        return f"Company({self.name})"