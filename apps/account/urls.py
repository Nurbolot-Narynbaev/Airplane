from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegistrationView,
    EmailActivationView,

    # PhoneActivationView,
    # ChangePasswordView,
    # SetRestoredPasswordView,
    # RestorePasswordView,

    DeleteAccountView,
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registartion'),
    path('activate/<str:activation_code>/', EmailActivationView.as_view(), name='activation'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]