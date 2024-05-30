from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ishare.models import ShareSongs
from song.models import Song
from songlist.models import SongList
from user.models import User
from .models import LikedSong, LikedSongList


@csrf_exempt
@require_http_methods(["GET"])
def liked_songs_get(request):
    try:
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'success': False, 'message': '未获取到用户名',
                                 'data': None, 'token': None}, status=400)

        user = User.objects.get(username=username)

        if not user.permission_liked_songs and request.role != 'admin' and request.username != username:
            return JsonResponse({'success': False,
                                 'message': '获取失败，用户设置为隐私'}, status=403)

        filtered_objects = LikedSong.objects.filter(user=user)
        songs_data = [obj.song.to_dict(request) for obj in filtered_objects if obj.song.visible]
        return JsonResponse({'success': True, 'message': '获取用户喜欢歌曲成功',
                             'data': songs_data, 'token': None}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在',
                             'data': None, 'token': None}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def liked_songs_add(request):
    try:
        song_id = request.POST.get('song_id')
        if not song_id:
            return JsonResponse({'success': False, 'message': '未获取到歌曲id',
                                 'data': None, 'token': None}, status=400)

        username = request.username
        if not username:
            return JsonResponse({'success': False, 'message': '未获取到用户名',
                                 'data': None, 'token': None}, status=400)

        user = User.objects.get(username=username)
        song = Song.objects.get(id=song_id)

        liked_song, created = LikedSong.objects.get_or_create(user=user, song=song)

        if created:
            song.like += 1
            song.save()
            message = '歌曲已添加到喜爱列表'
        else:
            message = '歌曲已在喜爱列表中'

        return JsonResponse({'success': True, 'message': message,
                             'data': None, 'token': None}, status=201)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在',
                             'data': None, 'token': None}, status=404)
    except Song.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌曲不存在',
                             'data': None, 'token': None}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def liked_songs_delete(request):
    try:
        song_id = request.POST.get('song_id')
        if not song_id:
            return JsonResponse({'success': False, 'message': '未获取到歌曲id',
                                 'data': None, 'token': None}, status=400)

        username = request.username
        if not username:
            return JsonResponse({'success': False, 'message': '未获取到用户名',
                                 'data': None, 'token': None}, status=400)

        user = User.objects.get(username=username)
        song = Song.objects.get(id=song_id)
        liked_song = LikedSong.objects.get(user=user, song=song)
        if liked_song:
            liked_song.delete()
            song.like -= 1
            if song.like < 0:
                song.like = 0
            song.save()
            return JsonResponse({'success': True, 'message': '歌曲已从喜爱列表中移除',
                                 'data': None, 'token': None}, status=200)
        else:
            return JsonResponse({'success': True, 'message': '歌曲不在喜爱列表中',
                                 'data': None, 'token': None}, status=200)

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在',
                             'data': None, 'token': None}, status=404)
    except Song.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌曲不存在',
                             'data': None, 'token': None}, status=404)
    except LikedSong.DoesNotExist:
        return JsonResponse({'success': False, 'message': '喜爱歌曲列表不存在',
                             'data': None, 'token': None}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def liked_songlists_add(request):
    try:
        songlist_id = request.POST.get('songlist_id')
        if not songlist_id:
            return JsonResponse({'success': False, 'message': '未获取到歌单id',
                                 'data': None, 'token': None}, status=400)

        username = request.username
        if not username:
            return JsonResponse({'success': False, 'message': '未获取到用户名',
                                 'data': None, 'token': None}, status=400)

        user = User.objects.get(username=username)
        songlist = SongList.objects.get(id=songlist_id)
        liked_songlist, created = LikedSongList.objects.get_or_create(user=user, songlist=songlist)
        if created:
            songlist.like += 1
            songlist.save()
            message = '歌单已添加到喜爱列表'
        else:
            message = '歌单已在喜爱列表中'

        return JsonResponse({'success': True, 'message': message,
                             'data': None, 'token': None}, status=201)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在',
                             'data': None, 'token': None}, status=404)
    except SongList.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌单不存在',
                             'data': None, 'token': None}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def liked_songlists_get(request):
    try:
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'success': False, 'message': '未获取到用户名',
                                 'data': None, 'token': None}, status=400)

        user = User.objects.get(username=username)
        filtered_objects = LikedSongList.objects.filter(user=user)
        songlists_data = [obj.songlist.to_sim_dict(request) for obj in filtered_objects if obj.songlist.visible]

        # 添加别人分享的歌单
        songlists_data += add_shared_songlists(user, request)

        return JsonResponse({'success': True, 'message': '获取用户喜欢歌单成功',
                             'data': songlists_data, 'token': None}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在',
                             'data': None, 'token': None}, status=404)


def add_shared_songlists(user, request):
    shares = ShareSongs.objects.filter(user=user)
    songlists = []
    for share in shares:
        share_user = share.shared_user
        # 构建分享者喜欢歌单的数据
        songlist = {
            'id': 'sh' + str(share_user.user_id),
            'title': share_user.username + '喜欢的歌曲',
            'cover': share_user.user_avatar(request),
            'owner': share_user.username,
            'create_date': share_user.registration_date.strftime('%Y-%m-%d %H:%M:%S'),
            'like': 1,
        }
        songlists.append(songlist)
    return songlists


@csrf_exempt
@require_http_methods(["POST"])
def liked_songlists_delete(request):
    try:
        songlist_id = request.POST.get('songlist_id')
        if not songlist_id:
            return JsonResponse({'success': False, 'message': '未获取到歌单id',
                                 'data': None, 'token': None}, status=400)

        username = request.username
        if not username:
            return JsonResponse({'success': False, 'message': '未获取到用户名',
                                 'data': None, 'token': None}, status=400)

        user = User.objects.get(username=username)

        if songlist_id.startswith('sh'):
            return delete_shared_songs(user, songlist_id)

        songlist = SongList.objects.get(id=songlist_id)

        liked_songlist = LikedSongList.objects.get(user=user, songlist=songlist)
        if liked_songlist:
            liked_songlist.delete()
            songlist.like -= 1
            if songlist.like < 0:
                songlist.like = 0
            songlist.save()
            return JsonResponse({'success': True, 'message': '歌单已从喜爱列表中移除',
                                 'data': None, 'token': None}, status=200)
        else:
            return JsonResponse({'success': True, 'message': '歌单不在喜爱列表中',
                                 'data': None, 'token': None}, status=200)

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在',
                             'data': None, 'token': None}, status=404)
    except SongList.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌单不存在',
                             'data': None, 'token': None}, status=404)
    except LikedSongList.DoesNotExist:
        return JsonResponse({'success': False, 'message': '喜爱歌单列表不存在',
                             'data': None, 'token': None}, status=404)


def delete_shared_songs(user, s_id):
    try:
        share_user_id = int(s_id[2:])
        share_user = User.objects.get(user_id=share_user_id)
        share = ShareSongs.objects.get(user=user, shared_user=share_user)
        share.delete()
        return JsonResponse({'success': True, 'message': '歌单已从喜爱列表中移除'}, status=200)

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
    except ShareSongs.DoesNotExist:
        return JsonResponse({'success': False, 'message': '分享记录不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
