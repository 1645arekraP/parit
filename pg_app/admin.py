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
    list_display = ('user', 'acceptance_rate', 'streak', 'friends_list', 'questions_list')
    
    def friends_list(self, obj):
        return ", ".join([friend.email for friend in obj.friends.all()])
    friends_list.short_description = 'Friends'

    def questions_list(self, obj):
        return obj.questions.count()
    questions_list.short_description = 'Number of Questions'

    search_fields = ('user__email', 'user__username')

#@admin.register(Solution)
#class SolutionAdmin(admin.ModelAdmin):
#    list_display = ('profile', 'question__title_slug', 'memory', 'runtime', 'accepted', 'date', 'attempts')
#    search_fields = ('question__title_slug', 'profile__user__email')
#    list_filter = ('accepted', 'tags')
#    ordering = ('-date',)
