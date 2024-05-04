from django.db import models

from user.models import User


# Create your models here.
class Complaint(models.Model):
    id = models.AutoField(primary_key=True)
    complainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complainer')
    complained = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complained')
    content = models.TextField()
    complaint_date = models.DateTimeField(auto_now_add=True)