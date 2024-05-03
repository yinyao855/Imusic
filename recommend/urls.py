from django.urls import path
from . import views

urlpatterns = [
    path('latest', views.get_recent_songs, name='latest'),
    # 获取推荐歌曲，暂定url为空，即/recommend/
    path('', views.get_recommended_songs, name='recommend'),
]