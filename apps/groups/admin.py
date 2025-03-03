from django.contrib import admin
from apps.groups.models import StudyGroup

@admin.register(StudyGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'invite_code', 'question_pool_type')
    search_fields = ('group_name', 'invite_code')
    list_filter = ('question_pool_type',)
    #ordering = ('group_name')