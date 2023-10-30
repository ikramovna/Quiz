from django.urls import path

from .views import CategoryListView, PostUserAnswerApiView, CategoryDetailView, SendMailAPIView

urlpatterns = [
    path('api/v1/category', CategoryListView.as_view()),
    path('api/v1/category/<int:pk>', CategoryDetailView.as_view()),
    path('api/v1/answer', PostUserAnswerApiView.as_view()),

    path('api/v1/send_mail', SendMailAPIView.as_view()),
]
