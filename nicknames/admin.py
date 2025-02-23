from django.contrib import admin
from .models import Nickname, Reaction

@admin.register(Nickname)
class NicknameAdmin(admin.ModelAdmin):
    list_display = ['given_to', 'given_by', 'nickname', 'created_at']
    list_filter = ['created_at']
    search_fields = ['given_to__email', 'given_by__email', 'nickname']

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'user', 'reaction_type']
    list_filter = ['reaction_type']
    search_fields = ['user__email', 'nickname__nickname'] 