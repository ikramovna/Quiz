from django.contrib import admin
from quize.models import Category, Question, Choice, UserAnswer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'category')
    list_filter = ('category',)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question', 'get_category')
    list_filter = ('question__category',)

    def get_category(self, obj):
        return obj.question.category

    get_category.short_description = 'Category'


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    ...


