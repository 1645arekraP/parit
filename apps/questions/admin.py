"""from django.contrib import admin
from apps.questions.models import Solution

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'question__title_slug', 'memory', 'runtime', 'accepted', 'date', 'attempts')
    search_fields = ('question__title_slug', 'profile__user__email')
    list_filter = ('accepted', 'tags')
    ordering = ('-date',)"""