from django.urls import path
from . import views
from follow import views as follow_views
from song import views as song_views
from songlist import views as songlist_views

urlpatterns = [
    path('register', views.user_register, name='register'),
    path('login', views.user_login, name='login'),
    path('info/<str:username>', views.get_user_info, name='info'),
    path('update/<str:username>', views.update_user_info, name='update'),
    path('delete/<str:username>', views.delete_user, name='delete'),
    path('alldata', views.get_all_users, name='all_info'),
    path('change-role', views.change_user_role, name='change_role'),
    path('change-pwd', views.change_password, name='change_pwd'),
    # 下面是得到用户创建的所有歌单
    path('songlists', songlist_views.get_user_songlists, name='get_user_songlists'),
    # 得到用户上传的所有歌曲
    path('songs', song_views.get_user_songs, name='get_user_songs'),
    # 发送验证码
    path('send-code', views.send_code, name='send_code'),
    # 关注或取消关注
    path('follow', follow_views.follow_unfollow, name='follow_unfollow'),
    # 获取关注列表
    path('followings', follow_views.get_followings, name='get_followings'),
    # 获取关注者列表
    path('followers', follow_views.get_followers, name='get_followers'),
]
