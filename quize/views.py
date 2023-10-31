from quize.serializers import CategoryListSerializer, CategoryDetailSerializer, UserAnswerSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
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






