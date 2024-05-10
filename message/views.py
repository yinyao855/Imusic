from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from message.models import Message
from user.models import User

from timedtask.utils import generate_user_weekly_report


# Create your views here.
# 发送消息
@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    try:
        sender_name = request.username
        receiver_name = request.POST.get('receiver')
        content = request.POST.get('content')

        sender = User.objects.get(username=sender_name)
        receiver = User.objects.get(username=receiver_name)

        with transaction.atomic():
            message = Message(sender=sender, receiver=receiver, title=sender_name, content=content, type=5)
            message.full_clean()
            message.save()

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


# 测试听歌周报
@csrf_exempt
@require_http_methods(["GET"])
def test(request):
    user = User.objects.get(username=request.username)
    res = generate_user_weekly_report(user, '2024-05-03', '2024-05-11')
    return JsonResponse({'success': True, 'message': '测试成功', 'data': res}, status=200)
