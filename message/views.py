from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from follow.models import Follow
from message.models import Message
from user.models import User

from timedtask.utils import generate_user_weekly_report, generate_user_upload_weekly_report

"""
发送消息函数，方便复用
:param title: 消息标题
:param content: 消息内容
:param message_type: 消息类型
:param sender: 发送者，如果为None，则表示系统发送
:param receiver: 接收者，如果为None，则表示发送给所有关注者
"""


def send_message(title, content, message_type, sender=None, receiver=None):
    try:
        messages = []
        if not receiver:
            followers = Follow.objects.filter(followed=sender)
            for follow in followers:
                message = Message(sender=sender, receiver=follow.follower, title=title, content=content,
                                  type=message_type)
                messages.append(message)
        else:
            message = Message(sender=sender, receiver=receiver, title=title, content=content, type=message_type)
            messages.append(message)

        with transaction.atomic():
            Message.objects.bulk_create(messages)

    except Exception as e:
        # 记录异常信息
        # logger.error(f"Error occurred while sending message: {str(e)}")
        # 回滚事务
        transaction.set_rollback(True)
        # 返回错误响应
        return JsonResponse({'success': False, 'message': 'Failed to send message'}, status=400)
    return JsonResponse({'success': True, 'message': 'Message sent successfully'})


# 发送消息(私信)
@csrf_exempt
@require_http_methods(["POST"])
def send(request):
    try:
        sender = User.objects.get(username=request.username)
        receiver_name = request.POST.get('receiver')
        receiver = User.objects.get(username=receiver_name)
        content = request.POST.get('content')
        if not content:
            return JsonResponse({'success': False, 'message': '消息内容不能为空'}, status=200)
        m_type = 5
        title = '私信'
        send_message(title, content, m_type, sender, receiver)

        return JsonResponse({'success': True, 'message': '消息发送成功'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


# 获取发送的消息
@csrf_exempt
@require_http_methods(["GET"])
def get_received_messages(request):
    try:
        receiver_name = request.username
        receiver = User.objects.get(username=receiver_name)
        messages = Message.objects.filter(receiver=receiver)
        message_list = [message.to_dict() for message in messages]
        return JsonResponse({'success': True, 'message': '获取用户消息成功', 'data': message_list}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


# 已读消息
@csrf_exempt
@require_http_methods(["POST"])
def read_message(request):
    try:
        message_id = request.POST.get('message_id')
        message = Message.objects.get(id=message_id)
        if message.receiver.username != request.username:
            return JsonResponse({'success': False, 'message': '这不是您的消息'}, status=403)
        message.is_read = True
        message.save()
        return JsonResponse({'success': True, 'message': '消息已读'}, status=200)
    except Message.DoesNotExist:
        return JsonResponse({'success': False, 'message': '消息不存在'}, status=400)


# 删除消息
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_message(request):
    try:
        message_id = request.GET.get('message_id')
        # print(message_id)
        message = Message.objects.get(id=message_id)
        if message.sender.username != request.username:
            return JsonResponse({'success': False, 'message': '无删除权限'}, status=403)
        message.delete()
        return JsonResponse({'success': True, 'message': '消息已删除'}, status=200)
    except Message.DoesNotExist:
        return JsonResponse({'success': False, 'message': '消息不存在'}, status=400)


# 测试周报
@csrf_exempt
@require_http_methods(["GET"])
def test(request):
    user = User.objects.get(username=request.username)
    res1 = generate_user_weekly_report(user, '2024-05-03', '2024-05-11')
    res2 = generate_user_upload_weekly_report(user, '2024-05-03', '2024-05-11')
    return JsonResponse({'success': True, 'message': '测试成功', 'data1': res1, "data2": res2}, status=200)
