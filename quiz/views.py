from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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
