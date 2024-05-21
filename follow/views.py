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
            if sender.following_count > 0:
                sender.following_count -= 1
            sender.save()
            if receiver.follower_count > 0:
                receiver.follower_count -= 1
            receiver.save()
            return JsonResponse({'success': True, 'message': '取消关注成功'}, status=200)
        else:
            # 加关注，发送关注信息
            Follow.objects.create(follower=sender, followed=receiver)
            Message.objects.create(sender=sender,
                                   receiver=receiver,
                                   title='新的关注',
                                   content=f'{sender_username}关注了你',
                                   type=5)
            sender.following_count += 1
            sender.save()
            receiver.follower_count += 1
            receiver.save()
            return JsonResponse({'success': True, 'message': '加关注成功'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '对象用户不存在'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_followings(request):
    username = request.GET.get('username')
    if not username:
        return JsonResponse({'success': False, 'message': '缺少对象用户的姓名'}, status=400)

    try:
        user = User.objects.get(username=username)
        if not user.permission_following and request.role != 'admin' and request.username != username:
            return JsonResponse({'success': False,
                                 'message': '获取失败，用户设置为隐私'}, status=403)
        followings = Follow.objects.filter(follower=user)
        following_list = [follow.followed.to_dict(request) for follow in followings]
        return JsonResponse({'success': True,
                             'message': '获取成功',
                             'data': following_list}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '对象用户不存在'}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def get_followers(request):
    username = request.GET.get('username')
    if not username:
        return JsonResponse({'success': False, 'message': '缺少对象用户的姓名'}, status=400)

    try:
        user = User.objects.get(username=username)
        if not user.permission_follower and request.role != 'admin' and request.username != username:
            return JsonResponse({'success': False,
                                 'message': '获取失败，用户设置为隐私'}, status=403)
        followers = Follow.objects.filter(followed=user)
        follower_list = [follow.follower.to_dict(request) for follow in followers]
        return JsonResponse({'success': True,
                             'message': '获取成功',
                             'data': follower_list}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '对象用户不存在'}, status=400)


# 获得用户的好友，互相关注为好友
@csrf_exempt
@require_http_methods(["GET"])
def get_friends(request):
    try:
        username = request.GET.get('username')
        user = User.objects.get(username=username)
        if request.role != 'admin' and request.username != username:
            return JsonResponse({'success': False,
                                 'message': '获取失败，用户设置为隐私'}, status=403)
        followings = Follow.objects.filter(follower=user)
        followers = Follow.objects.filter(followed=user)
        following_list = [follow.followed for follow in followings]
        follower_list = [follow.follower for follow in followers]
        friend_list = list(set(following_list).intersection(set(follower_list)))
        friend_list = [friend.to_dict(request) for friend in friend_list]
        return JsonResponse({'success': True,
                             'message': '获取成功',
                             'data': friend_list}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '对象用户不存在'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
