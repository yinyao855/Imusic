from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Follow
from user.models import User
from message.models import Message


@csrf_exempt
@require_http_methods(["POST"])
def follow_unfollow(request):
    sender_username = request.username
    receiver_username = request.POST.get('username')
    if not receiver_username:
        return JsonResponse({'success': False, 'message': '缺少对象用户的姓名'}, status=400)

    try:
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        existing_follow = Follow.objects.filter(follower=sender, followed=receiver).first()

        if existing_follow:
            # 取消关注，并且删除之前关注的时候发送的信息
            existing_follow.delete()
            Message.objects.filter(sender=sender,
                                   receiver=receiver,
                                   content=f'{sender_username}关注了你') \
                .delete()
            sender.following_count -= 1
            receiver.follower_count -= 1
            return JsonResponse({'success': True, 'message': '取消关注成功'}, status=200)
        else:
            # 加关注，发送关注信息
            Follow.objects.create(follower=sender, followed=receiver)
            Message.objects.create(sender=sender,
                                   receiver=receiver,
                                   content=f'{sender_username}关注了你',
                                   type=5)
            sender.following_count += 1
            receiver.follower_count += 1
            return JsonResponse({'success': True, 'message': '加关注成功'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '对象用户不存在'}, status=400)
