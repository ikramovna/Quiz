from rest_framework import serializers

from quize.models import Category, Question, Choice, UserAnswer


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'answer']


class QuestionSerializer(serializers.ModelSerializer):
    choice = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'choice']


class CategoryDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, source='question_set')

    class Meta:
        model = Category
        fields = ['questions']


class UserAnswerSerializers(serializers.Serializer):
    category_id = serializers.IntegerField()
    answers = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(),
            allow_empty=False
        )
    )
