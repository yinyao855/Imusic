from django.db import models
from imusic.constant import *
import user.models


class Song(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="歌曲ID")
    title = models.CharField(max_length=200, verbose_name="标题")
    singer = models.CharField(max_length=100, verbose_name="演唱者")
    cover = models.FileField(upload_to='covers/', verbose_name="封面图")
    introduction = models.TextField(blank=True, null=True, verbose_name="歌曲介绍")
    audio = models.FileField(upload_to='audios/', verbose_name="音频文件")
    lyric = models.FileField(upload_to='lyrics/', blank=True, null=True, verbose_name="歌词文件")
    minutes = models.IntegerField(verbose_name="长度（分钟）")
    seconds = models.IntegerField(verbose_name="长度（秒）")
    tag_theme = models.CharField(max_length=100, blank=True, null=True, choices=THEME_CHOICES, verbose_name="主题标签")
    tag_scene = models.CharField(max_length=100, blank=True, null=True, choices=SCENE_CHOICES, verbose_name="场景标签")
    tag_mood = models.CharField(max_length=100, blank=True, null=True, choices=MOOD_CHOICES, verbose_name="心情标签")
    tag_style = models.CharField(max_length=100, blank=True, null=True, choices=STYLE_CHOICES, verbose_name="风格标签")
    tag_language = models.CharField(max_length=50, blank=True, null=True, choices=LANGUAGE_CHOICES, verbose_name="语言标签")
    uploader = models.ForeignKey(user.models.User, on_delete=models.CASCADE, verbose_name="上传者")
    like = models.IntegerField(default=0, verbose_name="喜欢人数")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")

    def __str__(self):
        return self.title

    def total_length(self):
        """计算总长度，返回秒数"""
        return self.minutes * 60 + self.seconds

    class Meta:
        verbose_name = "歌曲"
        verbose_name_plural = "歌曲"
