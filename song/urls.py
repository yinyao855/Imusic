from django.urls import path
from . import views
from complaint import views as complaint_views

urlpatterns = [
    path('upload', views.song_upload, name='song_upload'),
    path('info/<str:songID>', views.get_song_info, name='get_song_info'),
    path('update/<str:songID>', views.update_song_info, name='update_song_info'),
    path('delete/<str:songID>', views.delete_song, name='delete_song'),
    path('alldata', views.get_all_songs, name='get_all_songs'),
    path('query', views.query_songs, name='query_songs'),
    # 获取歌曲评论
    path('comments', views.get_comments, name='get_comments'),
    # 投诉歌曲
    path('complaint', complaint_views.complain, name='complaint'),
    path('init_data', views.get_init_singer, name='get_init_singer')
]
