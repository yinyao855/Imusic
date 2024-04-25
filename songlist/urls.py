from django.urls import path
from . import views

urlpatterns = [
    path('create', views.songlist_create, name='create'),
    path('info/<str:songlistID>', views.get_songlist_info, name='info'),
    path('update/<str:songlistID>', views.update_songlist_info, name='update'),
    path('delete/<str:songlistID>', views.delete_songlist, name='delete'),
    path('alldata', views.get_all_songlists, name='all_info'),
    path('addsong', views.songlist_add, name='add_song'),
    path('delsong', views.songlist_remove, name='del_song'),
    path('initdata', views.get_init_songlists, name='get_init_songlists'),
]
