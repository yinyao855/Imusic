from django.db import models

from user.models import User


# Create your models here.
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
