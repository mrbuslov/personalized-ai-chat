from tortoise.models import Model
from tortoise import fields
import uuid


class AIConfiguration(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    global_prompt = fields.TextField(null=True)
    company = fields.ForeignKeyField("models.Company", related_name="ai_configurations")
    chat = fields.ForeignKeyField("models.Chat", related_name="ai_configurations", null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "ai_configurations"
        
    def __str__(self):
        config_type = "Global" if self.chat_id is None else f"Chat-specific ({self.chat_id})"
        return f"AIConfiguration({config_type})"