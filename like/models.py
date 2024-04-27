from django.db import models
from django.contrib.auth.models import User
from song.models import Song
from songlist.models import SongList


class LikedSongs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ManyToManyField(Song)


class LikedSongLists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songlist = models.ManyToManyField(SongList)
