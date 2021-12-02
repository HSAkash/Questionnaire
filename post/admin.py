from django.contrib import admin
from post import models

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'published_date')
    list_filter = ('published_date',)
    readonly_fields = ('user', 'id')
    search_fields = ('title', 'user')
    date_hierarchy = 'published_date'
    ordering = ['-published_date']
    filter_horizontal = ()
    fieldsets = ()

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user')
    # list_filter = ('user', 'question',)
    readonly_fields = ('user','question', 'id')
    search_fields = ('question', 'user')
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)
