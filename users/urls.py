from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import (UserRegisterCreateAPIView, CheckActivationCodeGenericAPIView, ResetPasswordView,
                         ResetPasswordConfirmView)

urlpatterns = [
    path('register', UserRegisterCreateAPIView.as_view()),
    path('activate-code', CheckActivationCodeGenericAPIView.as_view()),
    path('reset-password', ResetPasswordView.as_view()),
    path('reset-password-confirm', ResetPasswordConfirmView.as_view()),
    path('login', TokenObtainPairView.as_view()),

]
