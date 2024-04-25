import json
import os.path

from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from song.models import Song
from user.models import User
from .models import SongList
from django.conf import settings


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
        existing_songlist = SongList.objects.filter(title__iexact=data['title'],
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

        return JsonResponse({'success': True, 'message': '歌单创建成功'}, status=201)

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '所有者不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_songlist_info(request, songlistID):
    try:
        songlist = SongList.objects.get(id=songlistID)
    except SongList.DoesNotExist:
        # 如果歌单不存在，则返回404错误
        return JsonResponse({'success': False, 'message': '未找到对应歌单'}, status=404)
    # 获取包含的歌曲信息
    songlist_info = songlist.to_dict(request)

    return JsonResponse({'success': True, 'message': '获取歌单成功', 'data': songlist_info}, status=200)


# 向歌单添加歌曲
@csrf_exempt
@require_http_methods(["POST"])
def songlist_add(request):
    try:
        data = request.POST
        songlist_id = data.get('songlist_id')
        song_id = data.get('song_id')
        song = Song.objects.get(id=song_id)
        songlist = SongList.objects.get(id=songlist_id)
        songlist.add_song(song)

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
        song_id = data.get('song_id')
        song = Song.objects.get(id=song_id)
        songlist = SongList.objects.get(id=songlist_id)
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
        return JsonResponse({'success': True, 'message': '更新歌单成功'}, status=200)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_songlist(request, songlistID):
    try:
        # 尝试找到并删除指定的歌单
        songlist = SongList.objects.get(id=songlistID)
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
    songlists = SongList.objects.all()
    data = []
    for songlist in songlists:
        data.append(songlist.to_dict(request))

    return JsonResponse({'success': True, 'message': '获取成功', 'data': data}, status=200)


@require_http_methods(["GET"])
def get_init_songlists(request):
    # 前10个like数最多的歌单
    top_songlists = SongList.objects.order_by('-like')[:10]

    songlists_data = []
    for songlist in top_songlists:
        songlist_data = {
            'cover': request.build_absolute_uri(os.path.join(settings.MEDIA_URL, songlist.cover.url))
                if songlist.cover else None,
            'creator': songlist.owner.username,
            'name': songlist.title,
        }
        songlists_data.append(songlist_data)

    return JsonResponse({
        'success': True,
        'songlists': songlists_data
    })