from django.db import models
import os
from django.conf import settings

from song.models import Song


# Create your models here.
class User(models.Model):
    objects = None
    user_id = models.AutoField(primary_key=True, verbose_name="用户ID")
    username = models.CharField(max_length=50, unique=True, verbose_name="用户名")
    email = models.EmailField(max_length=50, null=True, blank=True, verbose_name="邮箱")
    password = models.CharField(max_length=50, verbose_name="密码")
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="注册日期")
    bio = models.TextField(blank=True, null=True, verbose_name="用户简介")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="头像")
    # 表示在数据库存储的是user，但是在显示的时候显示的是User
    role_choices = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=role_choices, default='user', verbose_name="角色")

    def __str__(self):
        return self.username

    def to_dict(self, request=None):
        avatar_url = request.build_absolute_uri(
            os.path.join(settings.MEDIA_URL, self.avatar.url)) if self.avatar else None
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'bio': self.bio if self.bio else None,
            'avatar': avatar_url,
            'role': self.role,
            'registration_date': self.registration_date.strftime('%Y-%m-%d %H:%M:%S')
        }


class Recent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    last_play = models.DateTimeField(auto_now_add=True, verbose_name="最后一次播放时间")

    class Meta:
        unique_together = (('user', 'song'),)  # 设置复合主键

