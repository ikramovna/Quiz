from django.urls import path
from quize.views import CategoryListAPIView, CategoryDetailAPIView, PostUserAnswerApiView

urlpatterns = [
    path('category/', CategoryListAPIView.as_view()),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view()),
    path('submit-answers/', PostUserAnswerApiView.as_view()),

]
