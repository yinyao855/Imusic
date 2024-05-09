from django.db import models
from imusic.constant import NOTICE_TYPE_CHOICES
from user.models import User


# Create your models here.
class Message(models.Model):
    DoesNotExist = None
    objects = None
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    title = models.CharField(max_length=50, null=True, verbose_name="消息标题")
    content = models.TextField(verbose_name="消息内容")
    type = models.IntegerField(choices=NOTICE_TYPE_CHOICES, default=1, verbose_name="消息类型")
    send_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.content

    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender.username,
            'receiver': self.receiver.username,
            'title': self.title,
            'content': self.content,
            'type': self.type,
            'send_date': self.send_date.strftime('%Y-%m-%d %H:%M:%S'),
            'is_read': self.is_read
        }
