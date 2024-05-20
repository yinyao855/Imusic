import os.path

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ishare.models import ShareSongs
from like.models import LikedSongList, LikedSong
from message.views import send_message
from song.models import Song
from user.models import User
from .models import SongList


@csrf_exempt
@require_http_methods(["POST"])
def songlist_create(request):
    try:
        data = request.POST
        required_fields = ['title', 'owner']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'success': False, 'message': f'缺少字段：{field}'}, status=400)

        cover_file = request.FILES.get('cover')
        if cover_file is None:
            return JsonResponse({'success': False, 'message': '缺少封面图'}, status=400)

        # 检查该歌单是否已经存在，大小写不敏感
        existing_songlist = SongList.objects.filter(visible=True, title__iexact=data['title'],
                                                    owner__username__iexact=data['owner'])
        if existing_songlist.exists():
            return JsonResponse({'success': False, 'message': '歌单已存在'}, status=400)

        # 获取创建者/所有者
        owner = User.objects.get(username=data['owner'])
        # 创建新的歌单实例
        new_songlist = SongList(
            title=data['title'],
            introduction=data.get('introduction', ''),
            cover=cover_file,
            tag_theme=data.get('tag_theme', ''),
            tag_scene=data.get('tag_scene', ''),
            tag_mood=data.get('tag_mood', ''),
            tag_style=data.get('tag_style', ''),
            tag_language=data.get('tag_language', ''),
            owner=owner
        )
        new_songlist.save()

        """
        发送消息给关注者
        """
        content = f'我新创建了歌单{new_songlist.title}，快来看看吧!'
        # 消息类型为5，详细解释见song/views 里的 song_upload部分
        m_type = 5
        title = "私信"
        send_message(title, content, m_type, sender=owner)

        return JsonResponse({'success': True, 'message': '歌单创建成功', 'id': new_songlist.id}, status=201)

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '所有者不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def add_shared_songs(request, songlistID):
    try:
        # 获取用户id
        user_id = int(songlistID[2:])
        friend = User.objects.get(user_id=user_id)
        cur_user = User.objects.get(username=request.GET.get('username'))
        # 判断分享是否存在
        share = ShareSongs.objects.filter(user=cur_user, shared_user=friend).first()
        if not share:
            return JsonResponse({'success': False, 'message': '分享不存在'}, status=404)
        # 查询分享者喜欢的歌曲
        liked = LikedSong.objects.filter(user=friend)
        info = {
            'id': songlistID,
            'title': friend.username + '喜欢的歌曲',
            'cover': friend.user_avatar(request),
            'introduction': '这是' + friend.username + '喜欢的歌曲',
            'songs': [like.song.to_dict(request) for like in liked if like.song.visible],
            "tag_theme": "null",
            "tag_scene": "null",
            "tag_mood": "null",
            "tag_style": "null",
            "tag_language": "null",
            "owner": friend.username,
            "create_date": friend.registration_date.strftime('%Y-%m-%d %H:%M:%S'),
            "like": 1,
            "user_favor": True
        }
        return JsonResponse({'success': True, 'message': '获取歌单成功', 'data': info}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def get_songlist_info(request, songlistID):
    try:
        if songlistID.startswith('sh'):
            return add_shared_songs(request, songlistID)

        songlist = SongList.objects.get(id=songlistID)
        # 获取包含的歌曲信息
        songlist_info = songlist.to_dict(request)

        # 如果用户已登录，检查用户是否已经喜欢该歌单
        username = request.GET.get('username', '')
        if username:
            user = User.objects.get(username=username)
            songlist_info['user_favor'] = LikedSongList.objects.filter(user=user, songlist=songlist).exists()

        return JsonResponse({'success': True, 'message': '获取歌单成功', 'data': songlist_info}, status=200)

    except SongList.DoesNotExist:
        # 如果歌单不存在，则返回404错误
        return JsonResponse({'success': False, 'message': '未找到对应歌单'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 向歌单添加歌曲
@csrf_exempt
@require_http_methods(["POST"])
def songlist_add(request):
    try:
        data = request.POST
        songlist_id = data.get('songlist_id')
        songlist = SongList.objects.get(id=songlist_id)

        if request.role != 'admin' and request.username != songlist.owner.username:
            return JsonResponse({'success': False, 'message': '没有权限操作'}, status=403)

        song_id = data.get('song_id')
        song = Song.objects.get(id=song_id)
        songlist.add_song(song)

        """
        发送消息给关注者
        """
        sender_name = request.username
        sender = User.objects.get(username=sender_name)
        content = f'我在歌单{songlist.title}中新添加了歌曲《{song.title}》，快来看看吧!'
        m_type = 5
        title = "私信"
        send_message(title, content, m_type, sender=sender)

        return JsonResponse({'success': True, 'message': '添加歌曲成功'}, status=200)

    except Song.DoesNotExist:
        return JsonResponse({'success': False, 'message': '某些歌曲未上传，请先上传对应歌曲'}, status=404)
    except SongList.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌单不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 从歌单中删除歌曲
@csrf_exempt
@require_http_methods(["POST"])
def songlist_remove(request):
    try:
        data = request.POST
        songlist_id = data.get('songlist_id')
        songlist = SongList.objects.get(id=songlist_id)

        if request.role != 'admin' and request.username != songlist.owner.username:
            return JsonResponse({'success': False, 'message': '没有权限操作'}, status=403)

        song_id = data.get('song_id')
        song = Song.objects.get(id=song_id)
        songlist.remove_song(song)

        return JsonResponse({'success': True, 'message': '删除歌曲成功'}, status=200)

    except Song.DoesNotExist:
        return JsonResponse({'success': False, 'message': '某些歌曲未上传，请先上传对应歌曲'}, status=404)
    except SongList.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌单不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def update_songlist_info(request, songlistID):
    try:
        songlist = SongList.objects.get(id=songlistID)
    except SongList.DoesNotExist:
        return JsonResponse({'success': False, 'message': '未找到对应歌单'}, status=404)

    try:
        data = request.POST

        if request.role != 'admin' and request.username != songlist.owner.username:
            return JsonResponse({'success': False, 'message': '没有权限操作'}, status=403)

        # 更新基本信息
        songlist.title = data.get('title', songlist.title)
        songlist.introduction = data.get('introduction', songlist.introduction)
        songlist.tag_theme = data.get('tag_theme', songlist.tag_theme)
        songlist.tag_scene = data.get('tag_scene', songlist.tag_scene)
        songlist.tag_mood = data.get('tag_mood', songlist.tag_mood)
        songlist.tag_style = data.get('tag_style', songlist.tag_style)
        songlist.tag_language = data.get('tag_language', songlist.tag_language)

        # 如果有更新封面的要求，那么就更新
        if 'cover' in request.FILES:
            # 先删除旧有封面
            if songlist.cover:
                cover_path = os.path.join(settings.MEDIA_ROOT, str(songlist.cover))
                try:
                    os.remove(cover_path)
                except FileNotFoundError:
                    pass
            songlist.cover = request.FILES['cover']

        songlist.save()

        """
        发送消息给关注者
        """
        sender_name = request.username
        sender = User.objects.get(username=sender_name)
        content = f'我更新了歌单{songlist.title}的信息，快来看看有什么变化吧!'
        m_type = 5
        title = "私信"
        send_message(title, content, m_type, sender=sender)

        return JsonResponse({'success': True, 'message': '更新歌单成功'}, status=200)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_songlist(request, songlistID):
    try:
        # 尝试找到并删除指定的歌单
        songlist = SongList.objects.get(id=songlistID)

        if request.role != 'admin' and request.username != songlist.owner.username:
            return JsonResponse({'success': False, 'message': '没有权限操作'}, status=403)

        # 删除歌单对应的封面图
        if songlist.cover:
            cover_path = os.path.join(settings.MEDIA_ROOT, str(songlist.cover))
            try:
                os.remove(cover_path)
            except FileNotFoundError:
                pass
        songlist.delete()
        return JsonResponse({'success': True, 'message': '删除歌单成功'}, status=200)
    except SongList.DoesNotExist:
        # 如果歌单不存在，返回一个404错误
        return JsonResponse({'success': False, 'message': '歌单不存在'}, status=404)
    except Exception as e:
        # 如果有其他错误发生，返回个500错误
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_all_songlists(request):
    songlists = SongList.objects.filter(visible=True)
    data = []
    for songlist in songlists:
        data.append(songlist.to_sim_dict(request))

    return JsonResponse({'success': True, 'message': '获取成功', 'data': data}, status=200)


@csrf_exempt
@require_http_methods(["GET"])
def get_user_songlists(request):
    try:
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'success': False, 'message': '缺少用户姓名'}, status=400)
        # 如果用户不存在，get会抛出异常
        user = User.objects.get(username=username)
        # 获取该用户的所有歌单
        user_songlists = SongList.objects.filter(owner=user)
        songlists_data = [songlist.to_sim_dict(request) for songlist in user_songlists if songlist.visible]
        return JsonResponse({'success': True, 'message': '获取用户歌单成功', 'data': songlists_data}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
