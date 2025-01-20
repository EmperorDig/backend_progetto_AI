from django.urls import path
from . import views

urlpatterns = [
    path('audio/', views.AudioListCreateView, name='audio-list-create'),
    path('add_audio/', views.AudioCreateView, name='audio-list-create'),
]