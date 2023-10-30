from django.urls import path

from users.views import (UserRegisterCreateAPIView, CheckActivationCodeGenericAPIView, ResetPasswordView,
                         ResetPasswordConfirmView)

urlpatterns = [
    path('register', UserRegisterCreateAPIView.as_view(), name='register'),
    path('activate-code', CheckActivationCodeGenericAPIView.as_view(), name='activate-code'),
    path('api/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('api/reset-password-confirm/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),
]