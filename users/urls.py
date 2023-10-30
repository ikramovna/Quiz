from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import (UserRegisterCreateAPIView, CheckActivationCodeGenericAPIView, ResetPasswordView,
                         ResetPasswordConfirmView)

urlpatterns = [
    path('api/v1/register', UserRegisterCreateAPIView.as_view()),
    path('api/v1/activate-code', CheckActivationCodeGenericAPIView.as_view()),
    path('api/v1/reset-password', ResetPasswordView.as_view()),
    path('api/v1/reset-password-confirm', ResetPasswordConfirmView.as_view()),
    path('api/v1/login', TokenObtainPairView.as_view()),

]
