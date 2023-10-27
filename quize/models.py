from django.db.models import CharField, TextField, ForeignKey, CASCADE, BooleanField

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
    question = ForeignKey('Question', CASCADE)
    answer = BooleanField()