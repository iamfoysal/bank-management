from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["email", "first_name", "account_number", "balance",]
    search_fields = ["email", "first_name", "last_name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name",
         "last_name", "account_number", "balance", "bank")}),
        ("Permissions", {"fields": ("is_active", "is_staff",
         "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )
    ordering = ["email"]


    def update_balance(self, request, queryset):
        for user in queryset:
            user.balance = 0
            user.save()
        self.message_user(request, "Balance updated successfully")

    update_balance.short_description = "Update balance to zero"

    actions = ["update_balance"]


admin.site.register(CustomUser, CustomUserAdmin)
