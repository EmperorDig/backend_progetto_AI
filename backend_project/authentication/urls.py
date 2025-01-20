from django.urls import path
from . import views

urlpatterns = [
    path('create-user/', views.createUser, name='create-user'),
]