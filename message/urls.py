from django.urls import path
from . import views

urlpatterns = [
    # 测试接口
    path('test', views.test),
    # 发送消息
    path('send', views.send, name='send'),
    # 获取消息
    path('', views.get_received_messages, name='received'),
    # 获取发送的消息
    path('get-sent', views.get_sent_messages, name='get_sent'),
    # 已读消息
    path('read', views.read_message, name='read'),
    # 删除消息
    path('delete', views.delete_message, name='delete'),
    # 私信查询
    path('private', views.search_private_messages, name='private'),
    # 查询聊天
    path('chats', views.search_chats, name='search'),
]
