from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', views.RegisterUser, name='create-user'),
    path('list-users/', views.ListUsers, name='list-users'),
    path('vista-protetta/', views.VIstaProtetta, name='vista-protetta'),

    # Endpoint per ottenere il token JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint per rinnovare il token
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
]