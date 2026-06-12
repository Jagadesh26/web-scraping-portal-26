from django.contrib import admin

from apps.accounts.models import (
    EmailVerificationToken,
    PasswordResetToken,
    User,
    UserSession,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_verified", "is_staff", "created_at")
    list_filter = ("is_active", "is_verified", "is_staff")
    search_fields = ("email",)
    readonly_fields = ("id", "created_at", "updated_at", "last_login")


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "device_name", "browser", "ip_address", "is_active", "last_activity")
    list_filter = ("is_active", "browser", "device_name")
    search_fields = ("user__email", "refresh_token_jti", "ip_address")
    readonly_fields = ("id", "refresh_token_jti", "created_at", "last_activity", "revoked_at")


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "expires_at", "used_at")
    list_filter = ("created_at", "expires_at", "used_at")
    search_fields = ("user__email",)
    readonly_fields = ("id", "token_hash", "created_at", "used_at")


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "expires_at", "used_at")
    list_filter = ("created_at", "expires_at", "used_at")
    search_fields = ("user__email",)
    readonly_fields = ("id", "token_hash", "created_at", "used_at")
