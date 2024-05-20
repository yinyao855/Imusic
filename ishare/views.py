import datetime
import random
import string

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ishare.models import Ishare, ShareSongs
from like.models import LikedSongList
from message.views import send_message
from songlist.models import SongList
from user.models import User


def generate_random_str(length=10):
    """
    生成一个指定长度的随机字符串，其中
    string.digits=0123456789
    string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for _ in range(length)]
    random_str = ''.join(str_list)
    return random_str


# 分享喜欢的歌曲
@csrf_exempt
@require_http_methods(["POST"])
def share_liked_songs(request):
    try:
        # 用户分享自己喜欢的歌曲给好友
        username = request.username
        user = User.objects.get(username=username)
        r_type = int(request.POST.get('type', 2))

        if r_type == 1:
            friend_name = request.POST.get('friend')
            friend = User.objects.get(username=friend_name)
            title = '分享动态'
            content = f"{user.username}分享了ta喜欢的歌曲给您，快来听听吧！"
            """
            发送消息给好友
            """
            _, m_id = send_message(title, content, 5, user, friend)
            if m_id:
                expire_date = datetime.datetime.now() + datetime.timedelta(days=1)
                ishare = Ishare(creator=user, s_type=0, content=m_id, obj_type=0, expire_date=expire_date)
                ishare.save()
            return JsonResponse({'success': True, 'message': '分享给好友成功'}, status=200)
        elif r_type == 2:
            f = generate_random_str()
            expire_date = datetime.datetime.now() + datetime.timedelta(days=1)
            ishare = Ishare(creator=user, s_type=1, content=f, obj_type=0, expire_date=expire_date)
            ishare.save()

            return JsonResponse({'success': True, 'message': '生成分享码成功', 'data': f}, status=200)

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 分享歌单
@csrf_exempt
@require_http_methods(["POST"])
def share_songlist(request):
    try:
        # 用户分享自己喜欢的歌曲给好友
        username = request.username
        user = User.objects.get(username=username)
        r_type = int(request.POST.get('type', 2))
        songlist_id = int(request.POST.get('songlist_id'))
        songlist = SongList.objects.filter(id=songlist_id, visible=True).first()

        if r_type == 1:
            friend_name = request.POST.get('friend')
            friend = User.objects.get(username=friend_name)
            title = '分享动态'
            content = f"{user.username}分享了歌单《{songlist.title}》给您，快来听听吧！"
            """
            发送消息给好友
            """
            _, m_id = send_message(title, content, 5, user, friend)
            if m_id:
                expire_date = datetime.datetime.now() + datetime.timedelta(days=1)
                ishare = Ishare(creator=user, s_type=0, content=m_id, obj_type=1, object_id=songlist_id,
                                expire_date=expire_date)
                ishare.save()
            return JsonResponse({'success': True, 'message': '分享给好友成功'}, status=200)
        elif r_type == 2:
            f = generate_random_str()
            expire_date = datetime.datetime.now() + datetime.timedelta(days=1)
            ishare = Ishare(creator=user, s_type=1, content=f, obj_type=1, object_id=songlist_id,
                            expire_date=expire_date)
            ishare.save()
            return JsonResponse({'success': True, 'message': '生成分享码成功', 'data': f}, status=200)

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
    except SongList.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌单不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 处理分享
@csrf_exempt
@require_http_methods(["POST"])
def handle_share(request):
    try:
        username = request.username
        user = User.objects.get(username=username)
        message_id = request.POST.get('message_id', '')
        code = request.POST.get('code', '')
        if not message_id and not code:
            return JsonResponse({'success': False, 'message': '参数不足'}, status=200)

        ishare = None
        if message_id:
            ishare = Ishare.objects.filter(content=message_id).first()
        elif code:
            ishare = Ishare.objects.filter(content=code).first()

        if ishare.expire_date < datetime.datetime.now():
            return JsonResponse({'success': False, 'message': '分享码不存在或已失效'}, status=200)

        if ishare.obj_type == 0:
            # 分享的是喜欢的歌曲
            ShareSongs.objects.get_or_create(user=user, shared_user=ishare.creator)
            return JsonResponse({'success': True, 'message': '接受分享成功'}, status=200)
        elif ishare.obj_type == 1:
            # 分享的是歌单
            songlist = SongList.objects.get(id=ishare.object_id)
            liked_songlist, created = LikedSongList.objects.get_or_create(user=user, songlist=songlist)
            if created:
                songlist.like += 1
                songlist.save()
                message = '接受分享成功，歌单已添加到收藏夹'
            else:
                message = '歌单已在收藏列表中'
            return JsonResponse({'success': True, 'message': message}, status=200)

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
    except Ishare.DoesNotExist:
        return JsonResponse({'success': False, 'message': '分享记录不存在'}, status=404)
    except SongList.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌单不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
