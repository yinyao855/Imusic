from django.urls import path
from . import views


urlpatterns = [
    # 关注或者取消关注, url为/follow
    path('', views.follow_unfollow, name='follow_unfollow'),
]