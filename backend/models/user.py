from tortoise.models import Model
from tortoise import fields
import uuid
from uuid import UUID

from fastadmin import TortoiseModelAdmin, WidgetType, register


class User(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    email = fields.CharField(max_length=255, unique=True)
    password_hash = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)
    company = fields.ForeignKeyField("models.Company", related_name="users")
    is_superuser = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Reverse relations
    chats = fields.ReverseRelation["Chat"]

    class Meta:
        table = "users"

    def __str__(self):
        return f"User({self.email})"


@register(User)
class UserAdmin(TortoiseModelAdmin):
    list_display = ("id", "email", "name", "is_superuser", "is_active")
    list_display_links = ("id", "email")
    list_filter = ("is_superuser", "is_active", "created_at")
    search_fields = ("email", "name")

    formfield_overrides = {  # noqa: RUF012
        "email": (WidgetType.EmailInput, {"required": True}),
        "password_hash": (
            WidgetType.PasswordInput,
            {"required": True, "label": "Password"},
        ),
    }

    async def create(self, request, data: dict) -> None:
        from services.auth_service import auth_service

        # Hash password before saving
        if "password_hash" in data:
            # Treat password_hash as plain password input and hash it
            plain_password = data["password_hash"]
            data["password_hash"] = auth_service.get_password_hash(plain_password)

        await super().create(request, data)

    async def update(self, request, data: dict) -> None:
        from services.auth_service import auth_service

        # Hash password if provided
        if "password_hash" in data and data["password_hash"]:
            # Treat password_hash as plain password input and hash it
            plain_password = data["password_hash"]
            data["password_hash"] = auth_service.get_password_hash(plain_password)
        elif "password_hash" in data and not data["password_hash"]:
            # Remove empty password field - don't update password
            data.pop("password_hash")

        await super().update(request, data)

    async def authenticate(self, email: str, password: str) -> int | None:
        from services.auth_service import auth_service
        from common.settings import settings

        # Only allow superadmin login
        if email != settings.superadmin_email:
            return None

        user = await auth_service.authenticate_user(email, password)
        if user and user.is_superuser:
            return user.id
        return None

    async def change_password(self, id: UUID | int, password: str) -> None:
        from services.auth_service import auth_service

        user = await self.model_cls.filter(id=id).first()
        if not user:
            return
        user.password_hash = auth_service.get_password_hash(password)
        await user.save(update_fields=("password_hash",))
