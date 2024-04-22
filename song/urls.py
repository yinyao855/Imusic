from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.song_upload, name='upload'),
    path('info/<str:songID>', views.get_song_info, name='info'),
    path('update/<str:songID>', views.update_song_info, name='update'),
    path('delete/<str:songID>', views.delete_song, name='delete'),
    path('alldata', views.get_all_songs, name='all_info'),
    path('query', views.query_songs, name='query')
]
