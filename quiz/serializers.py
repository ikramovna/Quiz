from rest_framework import serializers
from .models import Category, Question, Choice, UserAnswer


class CategorySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    def get_questions(self, obj):
        questions = Question.objects.filter(category=obj)
        result = []
        for question in questions:
            choices = Choice.objects.filter(question=question)
            result.append({
                "id": question.id, "question": question.question,
                "answer": [{"id": choice.id, "answer": choice.answer} for choice in choices]})
        return result

    class Meta:
        model = Category
        fields = ['questions']


class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description']


class UserAnswerSerializers(serializers.ModelSerializer):
    answers = serializers.ListField(child=serializers.DictField())

    class Meta:
        model = UserAnswer
        fields = ['category', 'answers']

    def create(self, validated_data):
        category = Category.objects.filter(pk=validated_data['category'].id).first()
        cor = 0
        for answer_data in validated_data['answers']:
            question = Question.objects.get(pk=answer_data['question_id'])
            choice = Choice.objects.get(pk=answer_data['answer_id'])
            user_answer, created = UserAnswer.objects.get_or_create(
                user=self.context["request"].user,
                category=category, question=question, defaults={'answer': choice})
            if not created:
                user_answer.answer = choice
                user_answer.save()
            if choice in question.choice.filter(is_correct=True):
                cor += 1
        return {"is_correct": cor, "count": len(validated_data['answers'])}


class SendEmailSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=500)
    name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=55)
    email = serializers.EmailField()