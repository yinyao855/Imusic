from django.db import models
from imusic.constant import *
from song.models import Song
from user.models import User


class SongList(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="歌单ID")
    title = models.CharField(max_length=200, verbose_name="歌单名称")
    cover = models.FileField(upload_to='covers/', verbose_name="封面图")
    introduction = models.TextField(blank=True, null=True, verbose_name="介绍")
    songs = models.ManyToManyField(Song, verbose_name="包含的歌曲")  # ManyToManyField 关联到Song模型
    tag_theme = models.CharField(max_length=100, blank=True, null=True, choices=THEME_CHOICES, verbose_name="主题标签")
    tag_scene = models.CharField(max_length=100, blank=True, null=True, choices=SCENE_CHOICES, verbose_name="场景标签")
    tag_mood = models.CharField(max_length=100, blank=True, null=True, choices=MOOD_CHOICES, verbose_name="心情标签")
    tag_style = models.CharField(max_length=100, blank=True, null=True, choices=STYLE_CHOICES, verbose_name="风格标签")
    tag_language = models.CharField(max_length=50, blank=True, null=True, choices=LANGUAGE_CHOICES, verbose_name="语言标签")
    like = models.IntegerField(default=0, verbose_name="喜欢人数")
    owner = models.ForeignKey(User, related_name='songlist_owner', on_delete=models.CASCADE, verbose_name="所有者")  # 外键关联到User模型
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="创建日期")  # 自动设置创建时间

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "歌单"
        verbose_name_plural = "歌单"
