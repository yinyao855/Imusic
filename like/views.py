from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import LikedSong, LikedSongList
from song.models import Song
from songlist.models import SongList
from user.models import User


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

        liked_songs = LikedSong.objects.filter(user=user)
        songs_data = [song.song.to_dict(request) for song in liked_songs if song.visible]
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
        liked_songlists = LikedSongList.objects.filter(user=user)
        songlists_data = [songlist.songlist.to_sim_dict(request) for songlist in liked_songlists if songlist.visible]
        return JsonResponse({'success': True, 'message': '获取用户喜欢歌单成功',
                             'data': songlists_data, 'token': None}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在',
                             'data': None, 'token': None}, status=404)


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
        songlist = SongList.objects.get(id=songlist_id)

        liked_songlist = LikedSongList.objects.get(user=user, songlist=songlist)
        if liked_songlist:
            liked_songlist.delete()
            songlist.like -= 1
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
