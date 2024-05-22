from django.urls import path
from . import views

urlpatterns = [
    path('upload/<str:singerid>', views.singer_update, name='update'),
    path('getsongs/<str:singerid>', views.singer_get_songs, name='get_info'),
]
