import json

from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Song
from user.models import User
import os
from django.conf import settings

@csrf_exempt
@require_http_methods(["POST"])
def song_upload(request):
    try:
        data = request.POST

        cover_file = request.FILES.get('cover')
        audio_file = request.FILES.get('audio')
        lyric_file = request.FILES.get('lyric')

        required_fields = ['title', 'singer', 'uploader']
        required_files = [cover_file, audio_file]  # lyric_file可选
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'success': False, 'message': f'缺少字段：{field}'}, status=400)
        for file in required_files:
            if file is None:
                return JsonResponse({'success': False, 'message': '缺少文件'}, status=400)

        user = User.objects.get(user_id=int(data['uploader']))
        song = Song(
            title=data['title'],
            singer=data['singer'],
            cover=cover_file,
            introduction=data.get('introduction', ''),
            audio=audio_file,
            lyric=lyric_file,
            tag_theme=data.get('tag_theme', ''),
            tag_scene=data.get('tag_scene', ''),
            tag_mood=data.get('tag_mood', ''),
            tag_style=data.get('tag_style', ''),
            tag_language=data.get('tag_language', ''),
            uploader=user,
            like=int(data.get('like', 0))
        )
        song.save()

        return JsonResponse({'success': True, 'message': '歌曲上传成功'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

# url version

# @require_http_methods(["POST"])
# def song_upload(request):
#     try:
#         data = request.POST
#         # 检查必要的字段是否存在
#         required_fields = ['title', 'singer', 'cover_url', 'audio_url',
#                            'minutes', 'seconds', 'uploader']
#         for field in required_fields:
#             if not data.get(field):
#                 return JsonResponse({'success': False, 'message': f'Missing required field: {field}'},
#                                     status=400)
#
#         # 创建歌曲实例
#         song = Song(
#             title=data['title'],
#             singer=data['singer'],
#             cover_url=data['cover_url'],
#             introduction=data.get('introduction', ''),
#             audio_url=data['audio_url'],
#             lyric_url=data.get('lyric_url', ''),
#             minutes=int(data['minutes']),
#             seconds=int(data['seconds']),
#             tag_theme=data.get('tag_theme', ''),
#             tag_scene=data.get('tag_scene', ''),
#             tag_mood=data.get('tag_mood', ''),
#             tag_style=data.get('tag_style', ''),
#             tag_language=data.get('tag_language', ''),
#             uploader_id=int(data['uploader']),
#             like=int(data.get('like', 0))
#         )
#         song.save()  # 保存到数据库
#
#         return JsonResponse({'success': True, 'message': '上传歌曲成功'})
#
#     except Exception as e:
#         return JsonResponse({'success': False, 'message': str(e)}, status=500)


def get_song_info(request, songID):
    if request.method == 'GET':
        try:
            song = Song.objects.get(id=songID)
        except Song.DoesNotExist:
            raise Http404("歌曲不存在")

        audio_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, song.audio.url))
        cover_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, song.cover.url)) if song.cover else None
        lyric_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, song.lyric.url)) if song.lyric else None
        song_info = {
            'id': song.id,
            'title': song.title,
            'singer': song.singer,
            'cover': cover_url,
            'introduction': song.introduction if song.introduction else None,
            'audio': audio_url,
            'lyric': lyric_url,
            'tag_theme': song.tag_theme if song.tag_theme else None,
            'tag_scene': song.tag_scene if song.tag_scene else None,
            'tag_mood': song.tag_mood if song.tag_mood else None,
            'tag_style': song.tag_style if song.tag_style else None,
            'tag_language': song.tag_language if song.tag_language else None,
            'uploader': song.uploader.username,
            'like': song.like,
            'upload_date': song.upload_date.strftime('%Y-%m-%d %H:%M:%S')
        }

        return JsonResponse(song_info)
    else:
        return JsonResponse({'error': '只允许GET请求'}, status=405)


@csrf_exempt
@require_http_methods(["PUT"])
def update_song_info(request, songID):
    try:
        song = Song.objects.get(id=songID)
    except Song.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌曲未找到'}, status=404)

    try:
        data = request.POST

        song.title = data.get('title', song.title)
        song.singer = data.get('singer', song.singer)
        song.introduction = data.get('introduction', song.introduction)
        song.tag_theme = data.get('tag_theme', song.tag_theme)
        song.tag_scene = data.get('tag_scene', song.tag_scene)
        song.tag_mood = data.get('tag_mood', song.tag_mood)
        song.tag_style = data.get('tag_style', song.tag_style)
        song.tag_language = data.get('tag_language', song.tag_language)

        # 对于文件字段（封面图、音频文件、歌词文件），需要特别处理
        if 'cover' in request.FILES:
            song.cover = request.FILES['cover']
        if 'audio' in request.FILES:
            song.audio = request.FILES['audio']
        if 'lyric' in request.FILES:
            song.lyric = request.FILES['lyric']

        song.save()

        return JsonResponse({'success': True, 'message': '更新成功'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 删除歌曲
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_song(request, songID):
    try:
        song = Song.objects.get(id=songID)
    except Song.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌曲未找到'}, status=404)

    try:
        song.delete()
        return JsonResponse({'success': True, 'message': '删除成功'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 获取所有歌曲信息
@csrf_exempt
def get_all_songs(request):
    if request.method == 'GET':
        songs = Song.objects.all()
        data = []
        for song in songs:
            cover_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, song.cover.url)) if song.cover else None
            audio_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, song.audio.url))
            lyric_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, song.lyric.url)) if song.lyric else None
            song_data = {
                'id': song.id,
                'title': song.title,
                'singer': song.singer,
                'cover': cover_url,
                'introduction': song.introduction if song.introduction else None,
                'audio': audio_url,
                'lyric': lyric_url,
                'tag_theme': song.tag_theme if song.tag_theme else None,
                'tag_scene': song.tag_scene if song.tag_scene else None,
                'tag_mood': song.tag_mood if song.tag_mood else None,
                'tag_style': song.tag_style if song.tag_style else None,
                'tag_language': song.tag_language if song.tag_language else None,
                'uploader': song.uploader.username,
                'like': song.like,
                'upload_date': song.upload_date.strftime('%Y-%m-%d %H:%M:%S')
            }
            data.append(song_data)
        return JsonResponse({'success': 1, 'message': '获取所有歌曲信息成功', 'data': data})

    return JsonResponse({'success': 0, 'message': '只允许GET请求'})

