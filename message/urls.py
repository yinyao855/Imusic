from django.urls import path
from . import views

urlpatterns = [
    # 测试接口
    path('test', views.test),
    # 发送消息
    path('send', views.send),
    # 获取消息
    path('', views.get_received_messages),
    # 获取发送的消息
    path('get-sent', views.get_sent_messages),
    # 已读消息
    path('read', views.read_message),
    # 删除消息
    path('delete', views.delete_message),
    # 私信查询
    path('private', views.search_private_messages),
    # 查询聊天
    path('chats', views.search_chats),
]
