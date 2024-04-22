from django.db import models
import os
from django.conf import settings


# Create your models here.
class User(models.Model):
    objects = None
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    registration_date = models.DateTimeField(auto_now_add=True)
    bio = models.TextField("用户简介", blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    # 表示在数据库存储的是user，但是在显示的时候显示的是User
    role_choices = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=role_choices, default='user')

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
