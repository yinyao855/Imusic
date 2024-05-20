from django.db import models

from user.models import User


# Create your models here.
class Ishare(models.Model):
    DoesNotExist = None
    objects = None
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator', verbose_name='创建者')
    s_type = models.IntegerField(default=0, verbose_name='分享类型')  # 0: 私发 1: 分享码
    content = models.CharField(max_length=16, null=True, verbose_name='分享内容')
    obj_type = models.IntegerField(null=True, verbose_name='分享对象类型')  # 0: 歌曲 1: 歌单
    object_id = models.IntegerField(null=True, verbose_name='分享对象id')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    expire_date = models.DateTimeField(verbose_name='过期时间')


class ShareSongs(models.Model):
    DoesNotExist = None
    objects = None
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_user', verbose_name='分享者')
