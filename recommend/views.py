from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from collections import defaultdict
from django.db.models import Q

from like.models import LikedSong
from song.models import Song
from user.models import User


# Create your views here.

# 查询最近上传歌曲
@csrf_exempt
@require_http_methods(['GET'])
def get_recent_songs(request):
    num = request.GET.get('num', 15)
    songs = Song.objects.all().order_by('-upload_date')
    # 默认返回最近上传的15首歌曲
    if num:
        songs = songs[:int(num)]
    songs_list = []
    for song in songs:
        songs_list.append(song.to_dict(request))
    return JsonResponse({'success': True, 'message': '获取最近歌曲成功', 'data': songs_list}, status=200)


@csrf_exempt
@require_http_methods(['GET'])
def get_recommended_songs(request):
    """
    推荐算法分为两个阶段：
        一是根据已记录的该用户的行为信息建立口味，
        二是在歌曲库里寻找最符合用户口味的20首歌曲
    目前建立口味的规则是：
        根据用户上传的歌曲和喜欢的歌曲的特征，为这个用户建立口味，这是一个字典数据结构
        口味字典里的key是歌曲的特征，例如歌曲标签里的轻音乐、伤感，还有歌曲作者；
        口味字典里的value是对应的权重，例如用户大量上传了霉霉的歌曲，那么霉霉对应的value就高
        具体见build_user_profile函数
    寻找最符合用户口味的歌曲的规则是：
        在歌曲库里首先排除用户曾经上传的和已经喜欢的（认为用户只想得到没听过的歌曲的推荐）
        遍历每一首歌曲，根据歌曲的特征和用户的口味字典得到该歌曲对于用户的权重值
        根据该权重值进行排序，返回20首权重值最高的歌曲
    """
    # 得到用户对象
    username = request.username
    user = User.objects.filter(username=username).first()
    # 建立用户口味
    user_profile = build_user_profile(user)
    # 推荐歌曲列表
    recommended_songs = recommend_songs(user, user_profile, request)

    return JsonResponse({'success': True, 'message': '获取推荐歌曲成功',
                         'data': recommended_songs}, status=200)


def build_user_profile(user):
    profile = defaultdict(int)
    # 默认用户上传的歌曲就是ta所喜欢的风格
    uploaded_songs = Song.objects.filter(uploader=user)
    for song in uploaded_songs:
        update_profile_from_song(song, profile)

    # 处理用户点过喜欢的歌曲
    liked_songs = LikedSong.objects.filter(user=user).select_related('song')
    for liked in liked_songs:
        update_profile_from_song(liked.song, profile)

    return profile


def update_profile_from_song(song, profile):
    # 歌手
    profile[song.singer] += 3
    # 标签类特征
    attributes = ['tag_theme', 'tag_scene', 'tag_mood', 'tag_style', 'tag_language']
    for attr in attributes:
        value = getattr(song, attr)
        print("test", song.tag_mood)
        if value:
            profile[value] += 1


def recommend_songs(user, profile, request):
    # 排除用户上传的和已经喜欢的歌曲
    excluded_songs = Song.objects.filter(Q(uploader=user) | Q(likedsong__user=user)).values_list('id', flat=True)
    songs = Song.objects.exclude(id__in=excluded_songs)
    recommendations = []
    # 本地测试，打印profile
    # print(profile)
    for song in songs:
        weight = 0
        # 计算权重
        weight += profile.get(song.singer, 0)
        attributes = ['tag_theme', 'tag_scene', 'tag_mood', 'tag_style', 'tag_language']
        for attr in attributes:
            value = getattr(song, attr)
            weight += profile.get(value, 0)
        recommendations.append((weight, song))

    # 按权重排序并选择前20首
    recommendations.sort(reverse=True, key=lambda x: x[0])
    return [song.to_dict(request) for _, song in recommendations[:20]]


