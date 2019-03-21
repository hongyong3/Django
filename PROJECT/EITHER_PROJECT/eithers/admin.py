from django.contrib import admin
from .models import Question, Answer

# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'issue_a', 'issue_b', 'image_a', 'image_b',)
admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('pick', 'comment', 'question_id',)
admin.site.register(Answer, AnswerAdmin)
