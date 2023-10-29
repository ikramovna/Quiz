import random

from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from mirahmad.models import Question, Choice, UserAnswer
from templated_mail.mail import BaseEmailMessage


class Messages:
    INVALID_CREDENTIALS_ERROR = _("Unable to log in with provided credentials.")
    INACTIVE_ACCOUNT_ERROR = _("User account is disabled.")
    INVALID_TOKEN_ERROR = _("Invalid token for given user.")
    INVALID_ACTIVATE_CODE_ERROR = _("Invalid activate code for given user.")
    INVALID_UID_ERROR = _("Invalid user id or user doesn't exist.")
    STALE_TOKEN_ERROR = _("Stale token for given user.")
    PASSWORD_MISMATCH_ERROR = _("The two password fields didn't match.")
    INVALID_PASSWORD_ERROR = _("Invalid password.")
    EMAIL_NOT_FOUND = _("User with given email does not exist.")
    CANNOT_CREATE_USER_ERROR = _("Unable to create account.")


class ActivationEmail(BaseEmailMessage):
    template_name = "activation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activation_code'] = random.randint(100000, 999999)

        setKey(
            key=context.get('email'),

            value=context.get('activation_code'),
            timeout=None
        )
        return context


def check_is_update(validated_data):
    if UserAnswer.objects.filter(category_id=validated_data['category'],
                                 user=validated_data['user']):
        print(validated_data)
        return True
    else:
        return False


def list_user_answers(user_answers):
    c = 0
    cor = 0
    for user_answer in user_answers:
        c += 1
        question = Question.objects.get(id=user_answer.question.id)
        choice_answer = Choice.objects.get(id=user_answer.answer.id)

        if find_is_correct(question, choice_answer):
            cor += 1

    d = {
        'is_correct': cor,
        'count': c,
    }
    return d


def find_is_correct(question, choice_answer):
    for i in question.choice.all():
        if i.id == choice_answer.id:
            return i.is_correct


def setKey(key, value, timeout=None):
    return cache.set(key, value, timeout=timeout)


def addKey(key, value, timeout=None):
    return cache.add(key, value, timeout=timeout)


def getKey(key):
    return cache.get(key)


def deleteKey(key):
    return cache.delete(key)


def getAllKey(pattern):
    return cache.keys(pattern)
