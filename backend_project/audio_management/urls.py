from django.urls import path
from .views import AudioListView, AudioCreateView

urlpatterns = [
    path('audiolist/', AudioListView, name='audio-list'),
    path('audiocreate/', AudioCreateView, name='audio-create'),
]