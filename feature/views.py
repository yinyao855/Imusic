from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from feature.models import Recent
from song.models import Song
from songlist.models import SongList
from user.models import User


# Create your views here.
@csrf_exempt
@require_http_methods(["GET"])
def get_recent(request):
    try:
        # username = request.GET.get('username')
        username = request.username
        if not username:
            return JsonResponse({'success': False, 'message': '未接收到用户姓名'})

        user = get_object_or_404(User, username=username)
        num = request.GET.get('num', 10)

        # 查询最近10首播放
        recent_plays = Recent.objects.filter(user=user).order_by('-last_play')

        if int(num) != -1:
            recent_plays = recent_plays[:int(num)]

        # song_list = [recent.to_dict(request) for recent in recent_plays]
        song_list = {
            'songs': [recent.song.to_dict(request) for recent in recent_plays],
        }

        return JsonResponse({'success': True, 'message': '查询最近播放歌曲成功', 'data': song_list}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 添加最近播放，如果列表里已经有这首歌，就更新时间，播放次数+1
@csrf_exempt
@require_http_methods(["POST"])
def add_recent(request):
    try:
        username = request.username
        song_id = request.POST.get('song_id')
        if not username or not song_id:
            return JsonResponse({'success': False, 'message': '未接收到用户姓名或歌曲id'})

        user = get_object_or_404(User, username=username)
        song = get_object_or_404(Song, id=song_id)

        # 查询是否已经存在这首歌
        recent = Recent.objects.filter(user=user, song=song).first()
        if recent:
            recent.last_play = timezone.now()
            recent.play_count += 1
            recent.w_play_count += 1
            recent.save()
        else:
            Recent.objects.create(user=user, song=song, play_count=1, w_play_count=1)

        return JsonResponse({'success': True, 'message': '添加最近播放成功'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 删除最近播放，测试阶段
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_recent(request):
    try:
        # username = request.GET.get('username')
        username = request.username
        song_id = request.GET.get('song_id')
        if not username or not song_id:
            return JsonResponse({'success': False, 'message': '未接收到用户姓名或歌曲id'})

        user = get_object_or_404(User, username=username)
        song = get_object_or_404(Song, id=song_id)

        # 查询是否已经存在这首歌
        recent = Recent.objects.filter(user=user, song=song).first()
        if recent:
            recent.delete()

        return JsonResponse({'success': True, 'message': '删除最近播放成功'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 热门歌单
@csrf_exempt
@require_http_methods(["GET"])
def get_hot_songlists(request):
    num = request.GET.get('num', 10)
    # 前num个like数最多的歌单
    top_songlists = SongList.objects.order_by('-like')[:int(num)]
    songlists_data = []
    for songlist in top_songlists:
        songlists_data.append(songlist.to_sim_dict(request))

    return JsonResponse({'success': True, 'message': '获取成功', 'data': songlists_data}, status=200)


# 热门歌曲
@csrf_exempt
@require_http_methods(["GET"])
def get_hot_songs(request):
    num = request.GET.get('num', 10)
    # 前num个like数最多的歌曲
    top_songs = Song.objects.order_by('-like')[:int(num)]
    songs_data = []
    for song in top_songs:
        songs_data.append(song.to_sim_dict(request))

    return JsonResponse({'success': True, 'message': '获取成功', 'data': songs_data}, status=200)
