from django.db import models

from user.models import User


# Create your models here.
class Complaint(models.Model):
    id = models.AutoField(primary_key=True)
    complainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complainer')
    complained = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complained')
    content = models.TextField()
    type_choices = (
        ('song', 'Song'),
        ('songlist', 'SongList'),
    )
    object_type = models.CharField(max_length=10, null=True, choices=type_choices, verbose_name="被投诉对象类型")
    object_id = models.IntegerField(null=True, verbose_name='被投诉对象id')
    complaint_date = models.DateTimeField(auto_now_add=True)

    def to_dict(self, request=None):
        if request.role != 'admin':
            return None

        return {
            'id': self.id,
            'complainer': self.complainer.username,
            'complained': self.complained.username,
            'content': self.content,
            'object_type': self.object_type,
            'object_id': self.object_id,
            'complaint_date': self.complaint_date,
        }
