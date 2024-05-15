from django.core.exceptions import ValidationError
from django.db import models
from imusic.constant import *
from song.models import Song
from user.models import User
from django.conf import settings
import os


class SongList(models.Model):
    DoesNotExist = None
    objects = None
    id = models.AutoField(primary_key=True, verbose_name="歌单ID")
    title = models.CharField(max_length=200, verbose_name="歌单名称")
    cover = models.FileField(upload_to='covers/', verbose_name="封面图")
    introduction = models.TextField(blank=True, null=True, verbose_name="介绍")
    songs = models.ManyToManyField(Song, verbose_name="包含的歌曲")  # ManyToManyField 关联到Song模型
    tag_theme = models.CharField(max_length=100, blank=True, null=True, choices=THEME_CHOICES, verbose_name="主题标签")
    tag_scene = models.CharField(max_length=100, blank=True, null=True, choices=SCENE_CHOICES, verbose_name="场景标签")
    tag_mood = models.CharField(max_length=100, blank=True, null=True, choices=MOOD_CHOICES, verbose_name="心情标签")
    tag_style = models.CharField(max_length=100, blank=True, null=True, choices=STYLE_CHOICES, verbose_name="风格标签")
    tag_language = models.CharField(max_length=50, blank=True, null=True, choices=LANGUAGE_CHOICES,
                                    verbose_name="语言标签")
    like = models.IntegerField(default=0, verbose_name="喜欢人数")
    owner = models.ForeignKey(User, related_name='songlist_owner', on_delete=models.CASCADE,
                              verbose_name="所有者")  # 外键关联到User模型
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="创建日期")  # 自动设置创建时间
    # 审核相关
    visible = models.BooleanField(default=True, verbose_name='是否可见')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "歌单"
        verbose_name_plural = "歌单"

    def to_dict(self, request=None):
        if not self.visible and request.role != 'admin':
            return None
        cover_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, self.cover.url)) if self.cover else None
        songs_data = [song.to_dict(request) for song in self.songs.all()]
        songlist_info = {
            'id': self.id,
            'title': self.title,
            'cover': cover_url,
            'introduction': self.introduction if self.introduction else None,
            'songs': songs_data,
            'tag_theme': self.tag_theme if self.tag_theme else None,
            'tag_scene': self.tag_scene if self.tag_scene else None,
            'tag_mood': self.tag_mood if self.tag_mood else None,
            'tag_style': self.tag_style if self.tag_style else None,
            'tag_language': self.tag_language if self.tag_language else None,
            'owner': self.owner.username,
            'create_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S'),
            'like': self.like,
            'user_favor': False,
        }

        return songlist_info

    def to_sim_dict(self, request=None):
        if not self.visible and request.role != 'admin':
            return None
        cover_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, self.cover.url)) if self.cover else None
        songlist_info = {
            'id': self.id,
            'title': self.title,
            'cover': cover_url,
            'owner': self.owner.username,
            'create_date': self.created_date.strftime('%Y-%m-%d %H:%M:%S'),
            'like': self.like,
        }

        return songlist_info

    # 添加歌曲到歌单
    def add_song(self, song):
        if not isinstance(song, Song):
            raise ValueError("The song must be an instance of Song model.")

        # 检查歌曲是否已经在歌单中
        if self.songs.filter(id=song.id).exists():
            raise ValidationError("The song is already in the song list.")

        # 添加歌曲到歌单
        self.songs.add(song)

    def remove_song(self, song):
        """
        从歌单中移除歌曲
        """
        if not isinstance(song, Song):
            raise ValueError("The song must be an instance of Song model.")

        # 检查歌曲是否在歌单中
        if not self.songs.filter(id=song.id).exists():
            raise ValidationError("The song is not in the song list.")

        # 从歌单中移除歌曲
        self.songs.remove(song)
