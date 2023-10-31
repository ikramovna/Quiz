from django.db import models
from shared.models import BaseModel


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class Question(BaseModel):
    category = models.ForeignKey('quize.Category', models.CASCADE)
    question = models.TextField()

    def __str__(self):
        return self.question


class Choice(BaseModel):
    question = models.ForeignKey('quize.Question', models.CASCADE, related_name='choice')
    answer = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class UserAnswer(BaseModel):
    user = models.ForeignKey('auth.User', models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    question = models.ForeignKey('quize.Question', models.CASCADE)
    answer = models.BooleanField()



