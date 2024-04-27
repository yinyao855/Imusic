from django.db import models
from user.models import User
from song.models import Song
from songlist.models import SongList


class LikedSong(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'song')


class LikedSongList(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songlist = models.ForeignKey(SongList, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'songlist')