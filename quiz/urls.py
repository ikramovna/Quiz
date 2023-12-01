from django.urls import path

from .views import CategoryListView, PostUserAnswerApiView, CategoryDetailView, SendMailAPIView, \
    UserAnswerStatistics, FeedbackAPIView, FeedBackListApiView

urlpatterns = [
    path('category', CategoryListView.as_view()),
    path('category/<int:pk>', CategoryDetailView.as_view()),
    path('answer', PostUserAnswerApiView.as_view()),
    path("history", UserAnswerStatistics.as_view()),
    path('send_mail', SendMailAPIView.as_view()),
    path('feedback', FeedbackAPIView.as_view()),
    path('feedback-list', FeedBackListApiView.as_view())
]
