from django.urls import path
from . import views
from complaint import views as complaint_views

urlpatterns = [
    path('create', views.songlist_create, name='create'),
    path('info/<str:songlistID>', views.get_songlist_info, name='get_songlist_info'),
    path('update/<str:songlistID>', views.update_songlist_info, name='update_songlist_info'),
    path('delete/<str:songlistID>', views.delete_songlist, name='delete_songlist'),
    path('alldata', views.get_all_songlists, name='get_all_songlists'),
    path('addsong', views.songlist_add, name='songlist_add'),
    path('delsong', views.songlist_remove, name='songlist_remove'),
    # 投诉歌单
    path('complaint', complaint_views.complain, name='complaint')
]
