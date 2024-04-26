from django.urls import path
from . import views

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
    path('songlists', views.get_user_songlists, name='get_user_songlists'),
]
