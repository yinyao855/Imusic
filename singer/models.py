import os

from django.db import models
from django.core.exceptions import ValidationError

from imusic import settings
from song.models import Song


# Create your models here.
class Singer(models.Model):
    objects = None
    singerID = models.AutoField(primary_key=True, verbose_name='歌手id')
    singerName = models.CharField(max_length=30, verbose_name='歌手姓名', null=True, blank=True)
    singerImage = models.FileField(upload_to='covers/', verbose_name="封面图", null=True, blank=True)
    songs = models.ManyToManyField(Song, verbose_name="包含的歌曲", related_name='songs')  # ManyToManyField 关联到Song模型

    def __str__(self):
        return self.singerName

    class Meta:
        verbose_name = "歌手"
        verbose_name_plural = "歌手"

    def add_song(self, song):
        if not isinstance(song, Song):
            raise ValueError("The song must be an instance of Song model.")

        if self.songs.filter(id=song.id).exists():
            raise ValidationError("The song is already in the song list.")

        self.songs.add(song)

    def remove_song(self, song):
        if not isinstance(song, Song):
            raise ValueError("The song must be an instance of Song model.")

        if not self.songs.filter(id=song.id).exists():
            raise ValidationError("The song not exists")

        self.songs.remove(song)

    def to_dict(self, request=None):
        cover_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, self.singerImage.url)) if self.singerImage else None
        songs_data = [song.to_dict(request) for song in self.songs.all() if song.visible]
        singer_info = {
            'id': self.singerID,
            'singerName': self.singerName,
            'singerImage': cover_url,
            'songs': songs_data,
        }

        return singer_info
