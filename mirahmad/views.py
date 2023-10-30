from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from mirahmad.models import Category
from mirahmad.serializers import CategorySerializer, CategoryListSerializers, UserAnswerSerializer


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
        if request.data['end'] is True:
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
