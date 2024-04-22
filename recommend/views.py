from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from song.models import Song


# Create your views here.

# 查询最近上传歌曲
@csrf_exempt
@require_http_methods(['GET'])
def get_recent_songs(request):
    songs = Song.objects.all().order_by('-upload_date')
    # 如果歌曲数量大于15，则只返回最近的15首歌曲
    if len(songs) > 15:
        songs = songs[:15]
    songs_list = []
    for song in songs:
        songs_list.append(song.to_dict(request))
    return JsonResponse({'success': True, 'message': '获取最近歌曲成功', 'data': songs_list}, status=200)
