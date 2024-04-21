import json
import os.path

from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ..song.models import Song
from ..user.models import User
from .models import SongList
from django.conf import settings


@csrf_exempt
def songlist_create(request):
    if request.method == 'POST':
        try:
            data = request.POST
            # 获取创建者/所有者
            owner = User.objects.get(user_id=data['owner'])
            # 创建新的歌单实例
            new_songlist = SongList(
                name=data['title'],
                introduction=data.get('introduction', ''),
                cover=request.FILES.get('cover', None),
                tag_theme=data.get('tag_theme', ''),
                tag_scene=data.get('tag_scene', ''),
                tag_mood=data.get('tag_mood', ''),
                tag_style=data.get('tag_style', ''),
                tag_language=data.get('tag_language', ''),
                owner=owner
            )
            new_songlist.save()

            # 添加歌曲到歌单
            song_ids = data.get('songs', [])
            for song_id in song_ids:
                song = Song.objects.get(id=song_id)
                new_songlist.songs.add(song)

            return JsonResponse({'success': True, 'message': '歌单创建成功'})

        except Song.DoesNotExist:
            return JsonResponse({'success': False, 'message': '某些歌曲未上传，请先上传对应歌曲'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    else:
        return JsonResponse({'success': False, 'message': '只允许POST请求'}, status=405)


def get_songlist_info(request, songlistID):
    if request.method == 'GET':
        try:
            songlist = SongList.objects.get(id=songlistID)
        except SongList.DoesNotExist:
            # 如果歌单不存在，则返回404错误
            raise Http404("歌单不存在")
        # 获取包含的歌曲信息
        songs_data = []
        for song in songlist.songs.all():
            cover_url = request.build_absolute_uri(
                os.path.join(settings.MEDIA_URL, song.cover.url)) if song.cover else None
            songs_data.append({
                'id': song.id,
                'title': song.title,
                'singer': song.singer,
                'cover': cover_url
            })

        cover_url = request.build_absolute_uri(
            os.path.join(settings.MEDIA_URL, songlist.cover.url)) if songlist.cover else None
        songlist_info = {
            'id': songlist.id,
            'title': songlist.name,
            'cover': cover_url,
            'introduction': songlist.introduction if songlist.introduction else None,
            'songs': songs_data,
            'tag_theme': songlist.tag_theme if songlist.tag_theme else None,
            'tag_scene': songlist.tag_scene if songlist.tag_scene else None,
            'tag_mood': songlist.tag_mood if songlist.tag_mood else None,
            'tag_style': songlist.tag_style if songlist.tag_style else None,
            'tag_language': songlist.tag_language if songlist.tag_language else None,
            'owner': songlist.owner.username,
            'create_date': songlist.created_date.strftime('%Y-%m-%d %H:%M:%S'),
            'like': songlist.like
        }

        return JsonResponse(songlist_info)
    else:
        return JsonResponse({'error': '只允许GET请求'}, status=405)


@csrf_exempt
@require_http_methods(["PUT"])
def update_songlist_info(request, songlistID):
    try:
        songlist = SongList.objects.get(id=songlistID)
    except SongList.DoesNotExist:
        return JsonResponse({'success': False, 'message': '未找到对应歌单'}, status=404)

    try:
        data = request.POST

        # 更新基本信息
        songlist.name = data.get('title', songlist.name)
        songlist.introduction = data.get('introduction', songlist.introduction)
        songlist.tag_theme = data.get('tag_theme', songlist.tag_theme)
        songlist.tag_scene = data.get('tag_scene', songlist.tag_scene)
        songlist.tag_mood = data.get('tag_mood', songlist.tag_mood)
        songlist.tag_style = data.get('tag_style', songlist.tag_style)
        songlist.tag_language = data.get('tag_language', songlist.tag_language)
        # 如果有更新封面的要求，那么就更新
        if 'cover' in request.FILES:
            songlist.cover = request.FILES['cover']

        # 更新包含的歌曲
        if 'songs' in data:
            songlist.songs.clear()  # 清除旧关联
            song_ids = data['songs']
            for song_id in song_ids:
                song = Song.objects.get(id=song_id)
                songlist.songs.add(song)

        songlist.save()

        return JsonResponse({'success': True, 'message': '更新成功'})
    except Song.DoesNotExist:
        return JsonResponse({'success': False, 'message': '存在歌曲未找到'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_songlist(request, songlistID):
    try:
        # 尝试找到并删除指定的歌单
        songlist = SongList.objects.get(id=songlistID)
        songlist.delete()
        return JsonResponse({'success': True, 'message': '删除歌单成功'})
    except SongList.DoesNotExist:
        # 如果歌单不存在，返回一个404错误
        return JsonResponse({'success': False, 'message': '歌单不存在'}, status=404)
    except Exception as e:
        # 如果有其他错误发生，返回个500错误
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
def get_all_songlists(request):
    if request.method == 'GET':
        songlists = SongList.objects.all()
        data = []
        for songlist in songlists:
            cover_url = request.build_absolute_uri(
                os.path.join(settings.MEDIA_URL, songlist.cover.url)) if songlist.cover else ''
            songs_data = [
                {
                    'id': song.id,
                    'title': song.title,
                    'singer': song.singer,
                    'cover': cover_url
                } for song in songlist.songs.all()
            ]

            songlist_data = {
                'id': songlist.id,
                'title': songlist.name,
                'cover': songlist.cover.url if songlist.cover else None,
                'introduction': songlist.introduction if songlist.introduction else None,
                'songs': songs_data,
                'tag_theme': songlist.tag_theme if songlist.tag_theme else None,
                'tag_scene': songlist.tag_scene if songlist.tag_scene else None,
                'tag_mood': songlist.tag_mood if songlist.tag_mood else None,
                'tag_style': songlist.tag_style if songlist.tag_style else None,
                'tag_language': songlist.tag_language if songlist.tag_language else None,
                'owner': songlist.owner.username,
                'create_date': songlist.created_date.strftime('%Y-%m-%d %H:%M:%S'),
                'like': songlist.like
            }
            data.append(songlist_data)

        return JsonResponse({'success': True, 'message': '获取成功', 'data': data})
    else:
        return JsonResponse({'success': False, 'message': '只允许GET请求'}, status=405)
