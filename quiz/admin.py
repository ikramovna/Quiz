from django.contrib import admin

from users.models import User
from .models import Category, Question, Choice


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ("category", "question")


@admin.register(Choice)
class ChoiceModelAdmin(admin.ModelAdmin):
    list_display = ("question", "answer", "is_correct")


class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'email', 'is_active', 'is_staff')
    search_fields = ('full_name', 'username', 'email')


admin.site.register(User, UserAdmin)
