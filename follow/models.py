from django.db import models

from user.models import User


# Create your models here.
class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')
    follow_date = models.DateTimeField(auto_now_add=True)
