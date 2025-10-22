from tortoise.models import Model
from tortoise import fields
import uuid

from fastadmin import TortoiseModelAdmin, WidgetType, register


class AIConfiguration(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    client_description = fields.TextField(null=True)
    special_instructions = fields.TextField(null=True)
    company = fields.ForeignKeyField("models.Company", related_name="ai_configurations")
    chat = fields.ForeignKeyField(
        "models.Chat", related_name="ai_configurations", null=True
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "ai_configurations"

    def __str__(self):
        config_type = (
            "Global" if self.chat_id is None else f"Chat-specific ({self.chat_id})"
        )
        return f"AIConfiguration({config_type})"


@register(AIConfiguration)
class AIConfigurationAdmin(TortoiseModelAdmin):
    list_display = ("id", "company", "chat", "created_at")
    list_display_links = ("id",)
    list_filter = ("created_at", "company", "chat")
    search_fields = ("client_description", "special_instructions")
    formfield_overrides = {  # noqa: RUF012
        "client_description": (WidgetType.TextArea, {"required": False}),
        "special_instructions": (WidgetType.TextArea, {"required": False}),
    }
