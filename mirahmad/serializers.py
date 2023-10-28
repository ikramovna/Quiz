import jwt
from django.contrib.auth.models import User
from rest_framework import serializers

from mirahmad.models import Category, Question, Choice, UserAnswer
from root.settings import SECRET_KEY


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['answer']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question']


class CategorySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField('get_questions')

    def get_questions(self, obj):
        questions = Question.objects.filter(category=obj)
        result = []
        for question in questions:
            d = {}
            d['id'] = question.id
            d['question'] = question.question
            choices = Choice.objects.filter(question=question)
            choices_data = [{"id": choice.id, "answer": choice.answer} for choice in choices]
            d['answer'] = choices_data
            result.append(d)
        return result

    class Meta:
        model = Category
        fields = ['questions']


class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description']


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        exclude = ['created_at', 'updated_at', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        if validated_data['end'] == False:
            return super().create(validated_data)
        elif validated_data['end'] == True:
            UserAnswer.objects.create(question=validated_data['question'],
                                      answer=validated_data['answer'],
                                      user=validated_data['user'],
                                      category=validated_data['category'],
                                      end=True)
            user_answers = UserAnswer.objects.filter(category_id=validated_data['category'])

            return list_user_answers(user_answers)


def list_user_answers(user_answers, c: int = 0, cor: int = 0):
    for user_answer in user_answers:
        c += 1
        question = Question.objects.get(id=user_answer.question.id)
        choice_answer = Choice.objects.get(id=user_answer.answer.id)

        if find_is_correct(question, choice_answer) == True:
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
