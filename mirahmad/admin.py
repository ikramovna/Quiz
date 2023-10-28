from django.contrib import admin
from mirahmad.models import UserAnswer, Category, Choice, Question

admin.site.register(UserAnswer)
admin.site.register(Category)


class AnswerInline(admin.StackedInline):
    model = Choice


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
