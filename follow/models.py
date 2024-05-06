from django.db import models

from user.models import User


# Create your models here.
class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name='关注者')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed', verbose_name='被关注者')
    follow_date = models.DateTimeField(auto_now_add=True)
