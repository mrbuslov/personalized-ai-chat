from tortoise.models import Model
from tortoise import fields
import uuid


class User(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    email = fields.CharField(max_length=255, unique=True)
    password_hash = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)
    company = fields.ForeignKeyField("models.Company", related_name="users")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    # Reverse relations
    chats = fields.ReverseRelation["Chat"]
    
    class Meta:
        table = "users"
        
    def __str__(self):
        return f"User({self.email})"