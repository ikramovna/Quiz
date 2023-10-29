from django.urls import path

from mirahmad.views import UserRegisterCreateAPIView, \
    CheckActivationCodeGenericAPIView

urlpatterns = [
    path('register', UserRegisterCreateAPIView.as_view(), name='register'),
    path('activate-code', CheckActivationCodeGenericAPIView.as_view(), name='activate-code'),
    # path('reset-passwd', PasswordResetGenericAPIView.as_view(), name='reset_passwd'),
    # path('reset-passwd-confirm', PasswordResetConfirmUpdateAPIView.as_view(), name='reset_passwd_confirm'),
]