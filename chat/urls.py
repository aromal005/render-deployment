from django.urls import path
from . views import *


urlpatterns = [
    
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOtpView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('token-refresh',CustomTokenRefreshView.as_view(),name='token-refresh')
]
