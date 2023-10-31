from rest_framework import serializers

from quize.models import Category, Question, Choice


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


class UserAnswerSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    answers = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(required=True, allow_null=False, min_value=1),
        ),
    )

# class ChoicesListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Choice
#         fields = ('answer',)
#
#
# class QuestionsListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ('question',)
#
#     def to_representation(self, instance: Question):
#         rep = super().to_representation(instance)
#         rep['answers'] = ChoicesListSerializer(instance, many=True).data
#         return rep
#
#
# class CategoryDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id',)
#
#     def to_representation(self, instance: Category):
#         rep = super().to_representation(instance)
#         rep['questions'] = QuestionsListSerializer(instance.question_set.all(), many=True).data
#         return rep
