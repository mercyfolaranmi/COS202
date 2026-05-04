from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Matric Info', {'fields': ('matric_number',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Matric Info', {'fields': ('matric_number',)}),
    )
    list_display = ['username', 'matric_number', 'email', 'first_name', 'last_name', 'is_staff']