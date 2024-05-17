from django.db import models
import os
from django.conf import settings


# Create your models here.
class User(models.Model):
    DoesNotExist = None
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
    follower_count = models.IntegerField(default=0, verbose_name="关注ta的人数")
    following_count = models.IntegerField(default=0, verbose_name="ta关注的人数")
    permission_email = models.BooleanField(default=True, verbose_name="是否公开邮箱")
    permission_follower = models.BooleanField(default=True, verbose_name="是否公开关注者")
    permission_following = models.BooleanField(default=True, verbose_name="是否公开正在关注的人")
    permission_registration_date = models.BooleanField(default=True, verbose_name="是否公开注册时间")
    permission_liked_songs = models.BooleanField(default=True, verbose_name="是否公开喜欢歌曲")

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
            'follower_count': self.follower_count,
            'following_count': self.following_count,
            'role': self.role,
            'registration_date': self.registration_date.strftime('%Y-%m-%d %H:%M:%S')
        }

    def to_pub_dict(self, request=None):
        avatar_url = request.build_absolute_uri(
            os.path.join(settings.MEDIA_URL, self.avatar.url)) if self.avatar else None
        return {
            'username': self.username,
            'email': self.email if self.permission_email else None,
            'bio': self.bio if self.bio else None,
            'avatar': avatar_url,
            'follower_count': self.follower_count,
            'following_count': self.following_count,
            'registration_date': self.registration_date.strftime('%Y-%m-%d %H:%M:%S') if self.permission_registration_date else None
        }

    def user_avatar(self, request=None):
        avatar_url = request.build_absolute_uri(
            os.path.join(settings.MEDIA_URL, self.avatar.url)) if self.avatar else None
        return avatar_url
