from django.db import models

from song.models import Song
from user.models import User


# Create your models here.
class Recent(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, verbose_name="歌曲")
    last_play = models.DateTimeField(auto_now_add=True, verbose_name="最近一次播放时间")
    play_count = models.IntegerField(default=0, verbose_name="播放次数")
    w_play_count = models.IntegerField(default=0, verbose_name="周播放次数")

    class Meta:
        unique_together = (('user', 'song'),)  # 设置复合主键

    def to_dict(self, request=None):
        return {
            'song': self.song.to_dict(request),
            'last_play': self.last_play.strftime('%Y-%m-%d %H:%M:%S'),
            'play_count': self.play_count,
            'w_play_count': self.w_play_count
        }

