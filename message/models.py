from django.db import models

from user.models import User


# Create your models here.
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
