from tortoise.models import Model
from tortoise import fields
import uuid

from fastadmin import TortoiseModelAdmin, WidgetType, register


class AIConfiguration(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    global_prompt = fields.TextField(null=True)
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
    search_fields = ("global_prompt",)
    formfield_overrides = {  # noqa: RUF012
        "global_prompt": (WidgetType.TextArea, {"required": False}),
    }
