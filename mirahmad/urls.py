from django.urls import path

from mirahmad.views import CategoryListView, UserAnswerApiView, CategoryDetailView

urlpatterns = [
    path('category/', CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category-list'),
    path('answer/', UserAnswerApiView.as_view(), name='user-answer-create'),
]
