from django.urls import path
from . import views

urlpatterns = [
    path('match-list/', views.MatchList, name='list-matches'),
    path('match-create/', views.MatchCreate, name='create-matches'),
]
