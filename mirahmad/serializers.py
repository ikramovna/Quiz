from rest_framework import serializers

from mirahmad.models import Category
from mirahmad.utils import *

error_messages = Messages()


# Api Serializers
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

    def to_representation(self, instance: Category):
        rep = super().to_representation(instance)
        questions = Question.objects.filter(category=instance)

        for question in questions:
            choices = Choice.objects.filter(question=question)
            rep['id'] = question.id
            rep['question'] = question.question
            rep['answer'] = [{"id": choice.id, "answer": choice.answer} for choice in choices]

            return rep

    # def get_questions(self, obj):
    #     questions = Question.objects.filter(category=obj)
    #     result = []
    #     for question in questions:
    #         choices = Choice.objects.filter(question=question)
    #         result.append({
    #             "id": question.id,
    #             "question": question.question,
    #             "answer": [{"id": choice.id, "answer": choice.answer} for choice in choices]
    #         })
    #     return result

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
        if validated_data['end'] is False:
            create_end_is_false(validated_data)
        elif validated_data['end'] is True:
            create_end_is_true(validated_data)
