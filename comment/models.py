from django.db import models

from song.models import Song
from user.models import User


# Create your models here.
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    content = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0, verbose_name="点赞人数")

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'song': self.song.id,
            'content': self.content,
            'comment_date': self.comment_date.isoformat(),
            'like': self.like
        }
