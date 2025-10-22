from tortoise.models import Model
from tortoise import fields
import uuid

from fastadmin import TortoiseModelAdmin, WidgetType, register


class Chat(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=255)
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


@register(Chat)
class ChatAdmin(TortoiseModelAdmin):
    list_display = ("id", "name", "user", "company", "created_at")
    list_display_links = ("id", "name")
    list_filter = ("created_at", "user", "company")
    search_fields = ("name",)
    formfield_overrides = {  # noqa: RUF012
        "name": (WidgetType.Input, {"required": True}),
    }
