from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User
from django.utils.translation import gettext_lazy as _

class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ['email', 'username']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']
    add_fieldsets = ((None, {'classes': ('wide', ), 'fields': ('email', 'password1', 'password2', 'username', 'is_active', 'is_staff', 'is_superuser')}),)

admin.site.register(User, UserAdmin)