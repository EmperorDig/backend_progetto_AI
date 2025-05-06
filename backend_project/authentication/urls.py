from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('register-patient/', views.RegisterPatient, name='create-patient'),
    path('register-doctor/', views.RegisterDoctor, name='create-doctor'),
    path('list-users/', views.ListUsers, name='list-users'),
    path('vista-protetta/', views.VIstaProtetta, name='vista-protetta'),

    # Endpoint per ottenere il token JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint per rinnovare il token
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    # Endpoint per verificare il token
    path('verify-token/', TokenVerifyView.as_view(), name='token_verify'),
]