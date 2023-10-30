from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from mirahmad.models import UserAnswer


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


def check_is_update(validated_data):
    return UserAnswer.objects.filter(
        category=validated_data['category'],
        user=validated_data['user']
    ).exists()


def list_user_answers(user_answers):
    user_answers = user_answers.select_related('question__choice')
    c = user_answers.count()
    cor = user_answers.filter(question__choice__is_correct=True).count()

    return {'is_correct': cor, 'count': c}


def find_is_correct(question, choice_answer):
    for i in question.choice.all():
        if i.id == choice_answer.id:
            return i.is_correct


def create_end_is_false(validated_data):
    if check_is_update(validated_data) is False:
        user_answer = UserAnswer(**validated_data)
        user_answer.save()
        return user_answer
    else:
        user_answer = UserAnswer.objects.filter(
            category=validated_data['category'],
            user=validated_data['user'],
            question=validated_data['question']
        ).first()
        if user_answer:
            for attr, value in validated_data.items():
                setattr(user_answer, attr, value)
            user_answer.save()
            return user_answer
        else:
            raise ValidationError("UserAnswer not found for update")


def create_end_is_true(validated_data):
    if check_is_update(validated_data) is False:
        UserAnswer(**validated_data).save()
        user_answers = UserAnswer.objects.filter(category=validated_data['category'])

        return list_user_answers(user_answers)
    else:
        user_answer = UserAnswer.objects.filter(
            category=validated_data['category'],
            user=validated_data['user'],
            question=validated_data['question']
        ).first()
        if user_answer:
            for attr, value in validated_data.items():
                setattr(user_answer, attr, value)
            user_answer.save()
            user_answers = UserAnswer.objects.filter(category=validated_data['category'])
            return list_user_answers(user_answers)
        else:
            raise ValidationError("UserAnswer not found for update")
