from django.urls import path
from . import views


urlpatterns = [
    # 发表评论
    path('add', views.add_comment, name='add_comment'),
    # 删除评论
    path('delete', views.delete_comment, name='delete_comment'),
]