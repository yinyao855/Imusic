from django.urls import path
from . import views

urlpatterns = [
    path('recent', views.get_recent, name='recent'),
    path('addrecent', views.add_recent, name='add'),
    path('delrecent', views.delete_recent, name='delete'),
    path('hotsongs', views.get_hot_songs, name='hot-songs'),
    path('hotsonglists', views.get_hot_songlists, name='hot-song-lists'),
    path('hotsingers', views.hot_singers, name='hot-singers')
]
