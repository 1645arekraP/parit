from django.contrib import admin
from .models import CustomUser, UserGroup, Profile, Solution

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'username')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('-date_joined',)

@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'invite_code', 'question_pool_type')
    search_fields = ('group_name', 'invite_code')
    list_filter = ('question_pool_type',)
    ordering = ('group_name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__email', 'user__username')

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'question_slug', 'memory', 'runtime', 'accepted', 'date', 'attempts')
    search_fields = ('question_slug', 'profile__user__email')
    list_filter = ('accepted', 'tags')
    ordering = ('-date',)
