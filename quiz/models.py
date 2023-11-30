from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import CharField, TextField, ForeignKey, CASCADE, BooleanField
from quiz.validators import phone_validator

from shared.models import BaseModel


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='categories')


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()


class Choice(BaseModel):
    question = ForeignKey('Question', CASCADE, related_name='choice')
    answer = CharField(max_length=200)
    is_correct = BooleanField(default=False)


class UserAnswer(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.ForeignKey("Choice", on_delete=models.CASCADE)


class History(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.ForeignKey("Choice", on_delete=models.CASCADE)
    uuid = models.CharField(max_length=500)


class Feedback(BaseModel):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13, validators=[phone_validator])
    email = models.EmailField()
    description = models.TextField()
