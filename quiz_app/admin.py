from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_type', 'difficulty', 'created_at')
    list_filter = ('question_type', 'difficulty')
    search_fields = ('question_text',)
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'is_correct', 'question')
    list_filter = ('is_correct',)
    search_fields = ('choice_text', 'question__question_text')
