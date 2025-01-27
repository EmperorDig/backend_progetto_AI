from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUser, name='create-user'),
    path('list-users/', views.ListUsers, name='list-users'),
]