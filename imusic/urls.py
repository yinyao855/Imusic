"""
URL configuration for imusic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from imusic.utils import check_token

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('users/', include('user.urls')),
                  path('songs/', include('song.urls')),
                  path('songlists/', include('songlist.urls')),
                  path('recommend/', include('recommend.urls')),
                  path('feature/', include('feature.urls')),
                  path('like/', include('like.urls')),
                  path('search/', include('search.urls')),
                  path('comments/', include('comment.urls')),
                  path('messages/', include('message.urls')),
                  path('timedtask/', include('timedtask.urls')),
                  path('complaints/', include('complaint.urls')),
                  path('check-token/', check_token, name='check_token'),
                  path('share/', include('ishare.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
