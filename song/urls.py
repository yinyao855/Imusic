from django.urls import path
from . import views
from complaint import views as complaint_views

urlpatterns = [
    path('upload', views.song_upload, name='upload'),
    path('info/<str:songID>', views.get_song_info, name='info'),
    path('update/<str:songID>', views.update_song_info, name='update'),
    path('delete/<str:songID>', views.delete_song, name='delete'),
    path('alldata', views.get_all_songs, name='all_info'),
    path('query', views.query_songs, name='query'),
    # 获取歌曲评论
    path('comments', views.get_comments, name='get_comments'),
    # 投诉歌曲
    path('complaint', complaint_views.complain, name='complaint'),
    path('init_data', views.get_init_singer, name='init_data')
]
