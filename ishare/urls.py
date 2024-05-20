from django.urls import path
from . import views


urlpatterns = [
    # 分享喜欢的歌曲
    path('likesongs', views.share_liked_songs, name='share_liked_songs'),
    # 分享歌单
    path('songlist', views.share_songlist, name='share_songlist'),
    # 处理分享
    path('handle', views.handle_share, name='handle_share'),
]
