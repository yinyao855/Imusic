from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import LikedSongs, LikedSongLists
from song.models import Song
from songlist.models import SongList
from user.models import User


@csrf_exempt
@require_http_methods(["GET"])
def liked_songs_get(request):
    if request.method == 'GET':
        try:
            username = request.GET.get('username')
            if not username:
                return JsonResponse({'success': False, 'message': '未获取到用户名'}, status=400)

            user = User.objects.get(username=username)
            liked_songs = LikedSongs.objects.get(user=user).song.all()
            songs_data = [song.to_dict(request) for song in liked_songs]
            return JsonResponse({'success': True, 'songs': songs_data})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def liked_songs_add(request):
    if request.method == 'POST':
        try:
            song_id = request.POST.get('song_id')
            if not song_id:
                return JsonResponse({'success': False, 'message': '未获取到歌曲id'}, status=400)

            username = request.POST.get('username')
            if not username:
                return JsonResponse({'success': False, 'message': '未获取到用户名'}, status=400)

            user = User.objects.get(username=username)
            song = Song.objects.get(id=song_id)

            liked_songs, created = LikedSongs.objects.get_or_create(user=user)
            liked_songs.song.add(song)

            song.like += 1
            song.save()
            return JsonResponse({'success': True, 'message': f'此时歌曲喜欢数为{song.like}'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
        except Song.DoesNotExist:
            return JsonResponse({'success': False, 'message': '歌曲不存在'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def liked_songs_delete(request):
    if request.method == 'POST':
        try:
            song_id = request.POST.get('song_id')
            if not song_id:
                return JsonResponse({'success': False, 'message': '未获取到歌曲id'}, status=400)

            username = request.POST.get('username')
            if not username:
                return JsonResponse({'success': False, 'message': '未获取到用户名'}, status=400)

            user = User.objects.get(username=username)
            song = Song.objects.get(id=song_id)

            liked_songs = LikedSongs.objects.get(user=user)
            if song in liked_songs.song.all():
                liked_songs.song.remove(song)
                song.like -= 1
                song.save()
                return JsonResponse({'success': True, 'message': '歌曲已从喜爱列表中移除'})
            else:
                return JsonResponse({'success': False, 'message': '歌曲不在喜爱列表中'}, status=404)

        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
        except Song.DoesNotExist:
            return JsonResponse({'success': False, 'message': '歌曲不存在'}, status=404)
        except LikedSongs.DoesNotExist:
            return JsonResponse({'success': False, 'message': '喜爱歌曲列表不存在'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def liked_songlists_add(request):
    if request.method == 'POST':
        try:
            songlist_id = request.POST.get('songlist_id')
            if not songlist_id:
                return JsonResponse({'success': False, 'message': '未获取到歌单id'}, status=400)

            username = request.POST.get('username')
            if not username:
                return JsonResponse({'success': False, 'message': '未获取到用户名'}, status=400)

            user = User.objects.get(username=username)
            songlist = SongList.objects.get(id=songlist_id)

            liked_songlists, created = LikedSongLists.objects.get_or_create(user=user)
            liked_songlists.songlist.add(songlist)

            songlist.like += 1
            songlist.save()
            return JsonResponse({'success': True, 'message': f'此时歌单喜欢数为{songlist.like}'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
        except SongList.DoesNotExist:
            return JsonResponse({'success': False, 'message': '歌单不存在'}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def liked_songlists_get(request):
    if request.method == 'GET':
        try:
            username = request.GET.get('username')
            if not username:
                return JsonResponse({'success': False, 'message': '未获取到用户名'}, status=400)

            user = User.objects.get(username=username)
            liked_songlists = LikedSongLists.objects.get(user=user).songlist.all()
            songlists_data = [songlist.to_dict(request) for songlist in liked_songlists]
            return JsonResponse({'success': True, 'songlists': songlists_data})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def liked_songlists_delete(request):
    if request.method == 'POST':
        try:
            songlist_id = request.POST.get('songlist_id')
            if not songlist_id:
                return JsonResponse({'success': False, 'message': '未获取到歌单id'}, status=400)

            username = request.POST.get('username')
            if not username:
                return JsonResponse({'success': False, 'message': '未获取到用户名'}, status=400)

            user = User.objects.get(username=username)
            songlist = SongList.objects.get(id=songlist_id)

            liked_songlists = LikedSongLists.objects.get(user=user)
            if songlist in liked_songlists.songlist.all():
                liked_songlists.songlist.remove(songlist)
                songlist.like -= 1
                songlist.save()
                return JsonResponse({'success': True, 'message': '歌单已从喜爱列表中移除'})
            else:
                return JsonResponse({'success': False, 'message': '歌单不在喜爱列表中'}, status=404)

        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)
        except SongList.DoesNotExist:
            return JsonResponse({'success': False, 'message': '歌单不存在'}, status=404)
        except LikedSongLists.DoesNotExist:
            return JsonResponse({'success': False, 'message': '喜爱歌单列表不存在'}, status=404)
