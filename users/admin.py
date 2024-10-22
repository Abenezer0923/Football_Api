from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CustomUser, Item

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Item)
