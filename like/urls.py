from django.urls import path
from . import views


urlpatterns = [
    # 获得喜爱歌曲
    path('songs', views.liked_songs_get, name='liked_songs_get'),
    # 添加喜爱歌曲
    path('songs/add', views.liked_songs_add, name='liked_songs_add'),
    # 获得喜爱歌单
    path('songlists', views.liked_songlists_get, name='liked_songlists_get'),
    # 添加喜爱歌单
    path('songlists/add', views.liked_songlists_add, name='liked_songlists_add'),
]
