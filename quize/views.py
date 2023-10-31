from rest_framework.parsers import FormParser, MultiPartParser

from quize.serializers import CategoryListSerializer, CategoryDetailSerializer, \
    UserAnswerSerializers
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from quize.models import Category, Question, Choice, UserAnswer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryDetailAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class PostUserAnswerApiView(CreateAPIView):
    serializer_class = UserAnswerSerializers

    def create(self, request, *args, **kwargs):
        category_id = request.data.get("category_id")
        answers_data = request.data.get("answers", [])
        total_questions = len(answers_data)
        correct_answers = 0

        for answer in answers_data:
            question_id = answer.get("question_id")
            answer_id = answer.get("answer_id")

            try:
                choice = Choice.objects.get(question_id=question_id, id=answer_id)
                if choice.is_correct:
                    correct_answers += 1
            except Choice.DoesNotExist:
                pass

        result_message = f"Your result: {correct_answers} from {total_questions}"

        response_data = {
            "result_message": result_message,
        }

        return Response(response_data, status=status.HTTP_200_OK)

