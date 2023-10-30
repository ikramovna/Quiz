from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from users.models import User
from .models import Category, Question, Choice


@admin.register(Category)
class CategoryModelAdmin(ImportExportModelAdmin):
    list_display = ("title", "description")


@admin.register(Question)
class QuestionModelAdmin(ImportExportModelAdmin):
    list_display = ("category", "question")


@admin.register(Choice)
class ChoiceModelAdmin(ImportExportModelAdmin):
    list_display = ("question", "answer", "is_correct")


class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'email', 'is_active', 'is_staff')
    search_fields = ('full_name', 'username', 'email')


admin.site.register(User, UserAdmin)
