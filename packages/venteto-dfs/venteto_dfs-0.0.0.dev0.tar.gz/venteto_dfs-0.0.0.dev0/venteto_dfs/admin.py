from django.contrib import admin

from .models import AuthUser


class AuthUserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "last_name", "first_name", "last_login"]
    list_filter = ["is_superuser", "is_staff", "is_active"]
    readonly_fields = ["uuid"]
    search_fields = ["username", "email", "last_name", "first_name"]

admin.site.register(AuthUser, AuthUserAdmin)
