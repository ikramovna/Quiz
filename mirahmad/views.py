from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from mirahmad.models import Category
from mirahmad.serializers import CategorySerializer, CategoryListSerializers, UserAnswerSerializer, \
    UserRegisterSerializer, getKey, CheckActivationCodeSerializer


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryListSerializers(categories, many=True)
        return Response(serializer.data)


class CategoryDetailView(APIView):

    def get(self, request, pk):
        try:
            instance = Category.objects.get(pk=pk)
        except Category.DoesNotExist as e:
            raise NotFound(e)

        serializer = CategorySerializer(instance)
        return Response(serializer.data.get("questions"))


class PostUserAnswerApiView(GenericAPIView):
    serializer_class = UserAnswerSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()
        if request.data['end'] == True:
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRegisterCreateAPIView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckActivationCodeGenericAPIView(GenericAPIView):
    serializer_class = CheckActivationCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = getKey(key=data['email'])['user']
        user.is_active = True
        user.save()
        return Response({"message": "Your email has been confirmed"},
                        status=status.HTTP_200_OK
                        )

# class PasswordResetGenericAPIView(GenericAPIView):
#     serializer_class = SendEmailResetSerializer
#     # parser_classes = (FormParser, MultiPartParser)
#     permission_classes = (AllowAny,)
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = serializer.validated_data.get('email')
#         return Response({'email': email}, status=status.HTTP_200_OK)
#
#
# class PasswordResetConfirmUpdateAPIView(GenericAPIView):
#     serializer_class = PasswordResetConfirmSerializer
#     permission_classes = (AllowAny,)
#
#     def patch(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         password = serializer.validated_data.get('new_password')
#         user = User.objects.get(email=serializer.validated_data.get('email'))
#         user.password = make_password(password)
#         user.save(update_fields=["password"])
#         return Response(status=status.HTTP_200_OK)


# {
#   "full_name": "mirahmad",
#   "email": "solihazohidova090909@gmail.com",
#   "username": "soliha",
#   "password": "admin"
# }
