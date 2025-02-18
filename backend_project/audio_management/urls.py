from django.urls import path
from .views import AudioListView, AudioCreateView, GetAudioData, PingView

urlpatterns = [
    path('audio-list/', AudioListView, name='audio-list'),
    path('audio-create/', AudioCreateView, name='audio-create'),
    path('audio-getdata/<int:audio_id>/', GetAudioData, name='audio-getdata'),
    path('ping/', PingView, name='ping-view')
]