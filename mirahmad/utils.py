from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from mirahmad.models import Question, Choice, UserAnswer


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
    if UserAnswer.objects.filter(category_id=validated_data['category'],
                                 user=validated_data['user']):
        print(validated_data)
        return True
    else:
        return False


def list_user_answers(user_answers):
    c, cor = 0, 0
    for user_answer in user_answers:
        c += 1
        question, choice_answer = Question.objects.get(id=user_answer.question.id), Choice.objects.get(
            id=user_answer.answer.id)
        if find_is_correct(question, choice_answer):
            cor += 1
    return {'is_correct': cor, 'count': c}


def find_is_correct(question, choice_answer):
    for i in question.choice.all():
        if i.id == choice_answer.id:
            return i.is_correct


def create_end_is_false(validated_data):
    if check_is_update(validated_data) is False:
        return super().create(validated_data)
    else:
        user_answer = UserAnswer.objects.filter(
            category_id=validated_data['category'],
            user=validated_data['user'],
            question_id=validated_data['question']
        ).first()
        if user_answer:
            return super().update(user_answer, validated_data)
        else:
            raise ValidationError("UserAnswer not found for update")


def create_end_is_true(validated_data):
    if check_is_update(validated_data) is False:
        UserAnswer.objects.create(validated_data)
        user_answers = UserAnswer.objects.filter(category_id=validated_data['category'])

        return list_user_answers(user_answers)
    else:
        user_answer = UserAnswer.objects.filter(
            category_id=validated_data['category'],
            user=validated_data['user'],
            question_id=validated_data['question']
        ).first()
        if user_answer:
            super().update(user_answer, validated_data)
            user_answers = UserAnswer.objects.filter(category_id=validated_data['category'])
            return list_user_answers(user_answers)
        else:
            raise ValidationError("UserAnswer not found for update")
