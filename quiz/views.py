from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .models import Category
from .serializers import CategoryListSerializers, CategorySerializer, UserAnswerSerializers, SendEmailSerializer
from .tasks import send_email_customer


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializers


class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostUserAnswerApiView(CreateAPIView):
    serializer_class = UserAnswerSerializers

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise AuthenticationFailed('You must be login')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()

        return Response(result, status=status.HTTP_201_CREATED)


class SendMailAPIView(GenericAPIView):
    serializer_class = SendEmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            message = serializer.validated_data.get('message')
            name = serializer.validated_data.get('name')
            phone = serializer.validated_data.get('phone')

            send_email_customer.delay(email, message, name, phone)
        except Exception as e:
            return Response({'success': False, 'message': str(e)})
        return Response({'success': True, 'message': 'You message successfully sent!'})


class UserAnswersListView(ListAPIView):
    def list(self, request, *args, **kwargs):
        user = request.user

        user_answers = UserAnswer.objects.filter(user=user)

        response_data = []

        categories = Category.objects.all()
        for category in categories:
            category_id = category.id
            question_count = 0
            is_correct = 0

            for user_answer in user_answers.filter(category=category):
                question_count += 1
                if user_answer.answer.is_correct:
                    is_correct += 1

            response_data.append({
                'category_id': category_id,
                'question_count': question_count,
                'is_correct': is_correct,
            })

        return Response(response_data)
