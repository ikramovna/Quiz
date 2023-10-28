from django.urls import path

from mirahmad.views import CategoryListView, PostUserAnswerApiView, CategoryDetailView

urlpatterns = [
    path('category/', CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category-list'),
    path('answer/', PostUserAnswerApiView.as_view(), name='user-answer-create'),
]
