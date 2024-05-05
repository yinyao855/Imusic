from django.urls import path
from . import views

urlpatterns = [
    path('songs', views.search_songs, name='search_songs'),
    path('songlists', views.search_songlists, name='search_songlists'),
    path('users', views.search_users, name='search_users'),
]
