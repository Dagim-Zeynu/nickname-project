from django.contrib import admin
from .models import Department, Profile

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'department', 'registration_complete']
    list_filter = ['department', 'registration_complete']
    search_fields = ['user__email', 'full_name'] 