from django.urls import path
from . import views

urlpatterns = [
    path('create', views.songlist_create, name='create'),
    path('info/<str:songlistID>', views.get_songlist_info, name='info'),
    path('update/<str:songlistID>', views.update_songlist_info, name='update'),
    path('delete/<str:songlistID>', views.delete_songlist, name='delete'),
    path('alldata', views.get_all_songlists, name='all_info'),
]
