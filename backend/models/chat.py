from tortoise.models import Model
from tortoise import fields
import uuid


class Chat(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=255)
    client_description = fields.TextField(null=True)
    special_instructions = fields.TextField(null=True)
    user = fields.ForeignKeyField("models.User", related_name="chats")
    company = fields.ForeignKeyField("models.Company", related_name="chats")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    # Reverse relations
    messages = fields.ReverseRelation["Message"]
    ai_configurations = fields.ReverseRelation["AIConfiguration"]
    
    class Meta:
        table = "chats"
        
    def __str__(self):
        return f"Chat({self.name})"