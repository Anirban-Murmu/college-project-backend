from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "first_name",
        "middle_name",
        "last_name",
        "is_active",
        "is_admin",
    )

    list_filter = (
        "is_active",
        "is_admin",
    )

    search_fields = (
        "email",
        "first_name",
        "middle_name",
        "last_name",
    )

    ordering = (
        "email",
    )

    fieldsets = (
        (
            "Personal Information",
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "email",
                    "image",
                    "gender",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "tc",
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    readonly_fields = (
        "last_login",
        "created_at",
        "updated_at",
    )