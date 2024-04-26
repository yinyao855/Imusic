from django.urls import path
from . import views

urlpatterns = [
    path('recent', views.get_recent, name='recent'),
    path('addrecent', views.add_recent, name='add'),
    path('delrecent', views.delete_recent, name='delete'),
]
