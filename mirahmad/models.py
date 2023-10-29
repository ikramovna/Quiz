from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import CharField, TextField, ForeignKey, CASCADE, BooleanField, EmailField, DateTimeField

from shared.models import BaseModel


class Category(BaseModel):
    title = CharField(max_length=255)
    description = TextField()


class Question(BaseModel):
    category = ForeignKey('Category', CASCADE)
    question = TextField()


class Choice(BaseModel):
    question = ForeignKey('Question', CASCADE, related_name='choice')
    answer = CharField(max_length=200)
    is_correct = BooleanField(default=False)


class UserAnswer(BaseModel):
    user = ForeignKey('User', CASCADE)
    category = ForeignKey("Category", CASCADE)
    question = ForeignKey('Question', CASCADE)
    answer = ForeignKey("Choice", CASCADE)
    end = BooleanField(default=False)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, full_name, email, password=None):
        if not username:
            raise ValueError('User not found username')
        if not email:
            raise ValueError('User not found email')

        user = self.model(
            username=username,
            full_name=full_name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, full_name, email, password=None):
        user = self.create_user(username, full_name, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'email']
