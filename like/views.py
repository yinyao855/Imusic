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
            return JsonResponse({'success': False, 'message': '未获取到用户名'}, status=400)

        user = User.objects.get(username=username)
        liked_songs = LikedSong.objects.filter(user=user)
        songs_data = [song.song.to_dict(request) for song in liked_songs]
        return JsonResponse({'success': True, 'songs': songs_data})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def liked_songs_add(request):
    try:
        song_id = request.POST.get('song_id')
        if not song_id:
            return JsonResponse({'success': False, 'message': '未获取到歌曲id'}, status=400)

        username = request.POST.get('username')
        if not username:
            return JsonResponse({'success': False, 'message': '未获取到用户名'}, status=400)

        user = User.objects.get(username=username)
        song = Song.objects.get(id=song_id)

        liked_song, created = LikedSong.objects.get_or_create(user=user, song=song)

        if created:
            song.like += 1
            song.save()
            flag = True
            message = f'此时歌曲喜欢数为{song.like}'
        else:
            flag = False
            message = '歌曲已在喜爱列表中'

        return JsonResponse({'success': flag, 'message': message})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
    except Song.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌曲不存在'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def liked_songs_delete(request):
    try:
        song_id = request.POST.get('song_id')
        if not song_id:
            return JsonResponse({'success': False, 'message': '未获取到歌曲id'}, status=400)

        username = request.POST.get('username')
        if not username:
            return JsonResponse({'success': False, 'message': '未获取到用户名'}, status=400)

        user = User.objects.get(username=username)
        song = Song.objects.get(id=song_id)

        liked_song = LikedSong.objects.get(user=user, song=song)
        if liked_song:
            liked_song.delete()
            song.like -= 1
            song.save()
            return JsonResponse({'success': True, 'message': '歌曲已从喜爱列表中移除'})
        else:
            return JsonResponse({'success': False, 'message': '歌曲不在喜爱列表中'}, status=404)

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
    except Song.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌曲不存在'}, status=404)
    except LikedSong.DoesNotExist:
        return JsonResponse({'success': False, 'message': '喜爱歌曲列表不存在'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def liked_songlists_add(request):
    try:
        songlist_id = request.POST.get('songlist_id')
        if not songlist_id:
            return JsonResponse({'success': False, 'message': '未获取到歌单id'}, status=400)

        username = request.POST.get('username')
        if not username:
            return JsonResponse({'success': False, 'message': '未获取到用户名'}, status=400)

        user = User.objects.get(username=username)
        songlist = SongList.objects.get(id=songlist_id)

        liked_songlists, created = LikedSongList.objects.get_or_create(user=user, songlist=songlist)
        if created:
            songlist.like += 1
            songlist.save()
            flag = True
            message = f'此时歌单喜欢数为{songlist.like}'
        else:
            flag = False
            message = '歌单已在喜爱列表中'

        return JsonResponse({'success': flag, 'message': message})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
    except SongList.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌单不存在'}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def liked_songlists_get(request):
    try:
        username = request.GET.get('username')
        if not username:
            return JsonResponse({'success': False, 'message': '未获取到用户名'}, status=400)

        user = User.objects.get(username=username)
        liked_songlists = LikedSongList.objects.filter(user=user)
        songlists_data = [songlist.to_dict(request) for songlist in liked_songlists]
        return JsonResponse({'success': True, 'songlists': songlists_data})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def liked_songlists_delete(request):
    try:
        songlist_id = request.POST.get('songlist_id')
        if not songlist_id:
            return JsonResponse({'success': False, 'message': '未获取到歌单id'}, status=400)

        username = request.POST.get('username')
        if not username:
            return JsonResponse({'success': False, 'message': '未获取到用户名'}, status=400)

        user = User.objects.get(username=username)
        songlist = SongList.objects.get(id=songlist_id)

        liked_songlist = LikedSongList.objects.get(user=user, songlist=songlist)
        if liked_songlist:
            liked_songlist.delete()
            songlist.like -= 1
            songlist.save()
            return JsonResponse({'success': True, 'message': '歌单已从喜爱列表中移除'})
        else:
            return JsonResponse({'success': False, 'message': '歌单不在喜爱列表中'}, status=404)

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
    except SongList.DoesNotExist:
        return JsonResponse({'success': False, 'message': '歌单不存在'}, status=404)
    except LikedSongList.DoesNotExist:
        return JsonResponse({'success': False, 'message': '喜爱歌单列表不存在'}, status=404)
