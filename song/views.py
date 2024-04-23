# Description: 歌曲相关视图函数
from django.core.exceptions import ValidationError
from mutagen.mp3 import MP3
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Song
from user.models import User
import os
from django.conf import settings
from django.db.models import Q
from django.db import transaction


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

        # 检查用户是否已经上传了相同的歌曲
        if Song.objects.filter(title=data['title'], singer=data['singer'],
                               uploader__username=data['uploader']).exists():
            return JsonResponse({'success': False, 'message': '您已经上传过这首歌曲了'}, status=400)

        # 检查音频文件类型
        if audio_file.content_type != 'audio/mpeg':
            return JsonResponse({'success': False, 'message': '音频文件格式必须为MP3'}, status=400)

        # 检查文件大小
        max_file_size = getattr(settings, "MAX_FILE_SIZE", 25 * 1024 * 1024)  # 默认为25MB
        max_file_size_2 = getattr(settings, "MAX_FILE_SIZE_2", 10 * 1024 * 1024)  # 默认为10MB
        if audio_file.size > max_file_size or cover_file.size > max_file_size_2:
            return JsonResponse({'success': False, 'message': '文件大小超过限制'}, status=400)

        # 发生了任何异常，整个数据库操作将会被回滚，保证了操作的原子性
        with transaction.atomic():
            user = User.objects.get(username=data['uploader'])
            duration = MP3(audio_file).info.length
            duration = str(duration)[:10]
            song = Song(
                title=data['title'],
                singer=data['singer'],
                cover=cover_file,
                introduction=data.get('introduction', ''),
                audio=audio_file,
                duration=duration,
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

        return JsonResponse({'success': True, 'message': '歌曲上传成功'}, status=201)

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '上传者不存在'}, status=400)

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

@csrf_exempt
@require_http_methods(["GET"])
def get_song_info(request, songID):
    try:
        song = Song.objects.get(id=songID)
    except Song.DoesNotExist as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=404)

    song_info = song.to_dict(request)

    return JsonResponse({'success': True, 'message': '获取歌曲信息成功', 'data': song_info}, status=200)


# 条件查询
@csrf_exempt
@require_http_methods(["GET"])
def query_songs(request):
    try:
        # 获取用户提供的查询参数
        query_params = {}
        for key in request.GET:
            value = request.GET.get(key)
            if value:
                query_params[key] = value

        # 如果没有提供任何搜索关键字，则返回错误消息
        if not query_params:
            return JsonResponse({'success': False, 'message': '缺少搜索关键字'}, status=400)

        # 构建查询条件
        query = Q()
        for key, value in query_params.items():
            query &= Q(**{f"{key}__contains": value})

        # 根据查询条件过滤歌曲
        songs = Song.objects.filter(query)

        # 将查询结果转换为字典格式
        data = [song.to_dict(request) for song in songs]

        return JsonResponse({'success': True, 'message': '搜索成功', 'data': data}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 通用查询，查询含有关键字的歌曲，用于搜索框
@csrf_exempt
@require_http_methods(["GET"])
def search_songs(request):
    try:
        keyword = request.GET.get('keyword', '')
        if not keyword:
            return JsonResponse({'success': False, 'message': '缺少搜索关键字'}, status=400)

        # 根据关键字查询歌曲，不区分大小写
        songs = Song.objects.filter(Q(title__icontains=keyword) | Q(singer__icontains=keyword) |
                                    Q(tag_theme__icontains=keyword) | Q(tag_scene__icontains=keyword) |
                                    Q(tag_mood__icontains=keyword) | Q(tag_style__icontains=keyword) |
                                    Q(tag_language__icontains=keyword))

        # 将查询结果转换为字典格式
        data = [song.to_dict(request) for song in songs]

        return JsonResponse({'success': True, 'message': '搜索成功', 'data': data}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 更新歌曲信息
@csrf_exempt
@require_http_methods(["POST"])
def update_song_info(request, songID):
    try:
        song = Song.objects.get(id=songID)
    except Song.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌曲未找到'}, status=404)

    try:
        data = request.POST

        # 更新歌曲信息
        update_fields = ['title', 'singer', 'introduction', 'tag_theme', 'tag_scene', 'tag_mood', 'tag_style',
                         'tag_language']
        for field in update_fields:
            setattr(song, field, data.get(field, getattr(song, field)))

        # 更新文件字段
        file_fields = {'cover': 'cover', 'audio': 'audio', 'lyric': 'lyric'}
        for field_name, field_attr in file_fields.items():
            if field_name in request.FILES:
                # 删除原有文件
                if getattr(song, field_attr):
                    file_path = os.path.join(settings.MEDIA_ROOT, str(getattr(song, field_attr)))
                    try:
                        os.remove(file_path)
                    except FileNotFoundError:
                        pass  # 文件不存在，继续执行后续代码
                setattr(song, field_attr, request.FILES[field_name])

        # 更新音频文件时更新 duration 字段
        if 'audio' in request.FILES:
            audio_duration = MP3(song.audio).info.length
            audio_duration = str(audio_duration)[:10]
            song.duration = audio_duration

        with transaction.atomic():
            song.full_clean()  # 执行完整性验证
            song.save()

        return JsonResponse({'success': True, 'message': '更新成功'}, status=200)
    except ValidationError as e:
        return JsonResponse({'success': False, 'message': e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 删除歌曲，目前是测试阶段
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_song(request, songID):
    try:
        song = Song.objects.get(id=songID)
    except Song.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌曲未找到'}, status=404)

    try:
        # 需要删除歌曲对应的封面、音频和歌词文件
        if song.cover:
            cover_path = os.path.join(settings.MEDIA_ROOT, str(song.cover))
            try:
                os.remove(cover_path)
            except FileNotFoundError:
                pass
        if song.audio:
            audio_path = os.path.join(settings.MEDIA_ROOT, str(song.audio))
            try:
                os.remove(audio_path)
            except FileNotFoundError:
                pass
        if song.lyric:
            lyric_path = os.path.join(settings.MEDIA_ROOT, str(song.lyric))
            try:
                os.remove(lyric_path)
            except FileNotFoundError:
                pass
        song.delete()
        return JsonResponse({'success': True, 'message': '删除成功'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 获取所有歌曲信息, 用于测试
@csrf_exempt
@require_http_methods(["GET"])
def get_all_songs(request):
    songs = Song.objects.all()
    data = []
    for song in songs:
        song_data = song.to_dict(request)
        data.append(song_data)
    return JsonResponse({'success': True, 'message': '获取所有歌曲信息成功', 'data': data}, status=200)

