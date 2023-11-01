from django.urls import path

from .views import CategoryListView, PostUserAnswerApiView, CategoryDetailView, SendMailAPIView, UserAnswersListView

urlpatterns = [
    path('category', CategoryListView.as_view()),
    path('category/<int:pk>', CategoryDetailView.as_view()),
    path('answer', PostUserAnswerApiView.as_view()),

    
     path('user/answer', UserAnswersListView.as_view()),
    path('send_mail', SendMailAPIView.as_view()),
]
