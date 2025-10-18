from tortoise.models import Model
from tortoise import fields
import uuid
from enum import Enum

from fastadmin import TortoiseModelAdmin, WidgetType, register


class MessageRole(str, Enum):
    CLIENT = "client"
    MANAGER = "manager"


class Message(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    content = fields.TextField()
    role = fields.CharEnumField(MessageRole, max_length=20)
    is_ai_generated = fields.BooleanField(default=False)
    chat = fields.ForeignKeyField("models.Chat", related_name="messages")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "messages"
        ordering = ["created_at"]

    def __str__(self):
        return f"Message({self.role}: {self.content[:50]}...)"


@register(Message)
class MessageAdmin(TortoiseModelAdmin):
    list_display = ("id", "role", "is_ai_generated", "chat", "created_at")
    list_display_links = ("id",)
    list_filter = ("role", "is_ai_generated", "created_at", "chat")
    search_fields = ("content",)
    formfield_overrides = {  # noqa: RUF012
        "content": (WidgetType.TextArea, {"required": True}),
        "role": (WidgetType.Select, {"required": True}),
    }
