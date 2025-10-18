from tortoise.models import Model
from tortoise import fields
import uuid
import typing as tp
from uuid import UUID

import bcrypt
from tortoise import fields
from tortoise.models import Model

from fastadmin import TortoiseModelAdmin, WidgetType, register


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
    
    

@register(User)
class UserAdmin(TortoiseModelAdmin):
    exclude = ("hash_password",)
    list_display = ("id", "username", "is_superuser", "is_active")
    list_display_links = ("id", "username")
    list_filter = ("id", "username", "is_superuser", "is_active")
    search_fields = ("username",)
    formfield_overrides = {  # noqa: RUF012
        "username": (WidgetType.SlugInput, {"required": True}),
        "password": (WidgetType.PasswordInput, {"passwordModalForm": True}),
        "avatar_url": (
            WidgetType.Upload,
            {
                "required": False,
                # Disable crop image for upload field
                # "disableCropImage": True,
            },
        ),
    }

    async def authenticate(self, email: str, password: str) -> int | None:
        user = await self.model_cls.filter(email=email, is_superuser=True).first()
        if not user:
            return None
        if not bcrypt.checkpw(password.encode(), user.hash_password.encode()):
            return None
        return user.id

    async def change_password(self, id: UUID | int, password: str) -> None:
        user = await self.model_cls.filter(id=id).first()
        if not user:
            return
        user.hash_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        await user.save(update_fields=("hash_password",))

    async def orm_save_upload_field(self, obj: tp.Any, field: str, base64: str) -> None:
        # convert base64 to bytes, upload to s3/filestorage, get url and save or save base64 as is to db (don't recomment it)
        setattr(obj, field, base64)
        await obj.save(update_fields=(field,))
