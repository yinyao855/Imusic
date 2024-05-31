import jieba
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from song.models import Song
from songlist.models import SongList
from user.models import User


# Create your views here.
# 通用查询，查询含有关键字的歌曲，用于搜索框
@csrf_exempt
@require_http_methods(["GET"])
def search_songs(request):
    try:
        # 停用词文件是 'stopwords.txt'
        with open('stopwords.txt', 'r', encoding='utf-8') as f:
            stopwords = set([line.strip() for line in f.readlines()])
        keyword = request.GET.get('keyword', '')
        num = request.GET.get('num', '')

        # 动态构建查询条件
        query = Q()

        if keyword:
            # 使用jieba对关键词进行分词
            keywords = list(set(jieba.cut_for_search(keyword)))
            filtered_words = [word for word in keywords if word not in stopwords]
            # print(filtered_words)
            if ' ' in keywords:
                keywords.remove(' ')

            for kw in filtered_words:
                query |= (Q(title__icontains=kw) | Q(singer__icontains=kw))

        fields = {
            'tag_theme': 'tag_theme',
            'tag_scene': 'tag_scene',
            'tag_mood': 'tag_mood',
            'tag_style': 'tag_style',
            'tag_language': 'tag_language',
            'uploader': 'uploader__username'
        }
        # 从请求参数中获取查询字段
        for field, field_name in fields.items():
            value = request.GET.get(field)
            if value:
                query &= Q(**{f"{field_name}__icontains": value})

        # 查询歌曲
        songs = Song.objects.filter(query)

        # 如果有num参数，返回指定数量的歌曲
        if num:
            songs = songs[:int(num)]

        # 将查询结果转换为字典格式
        data = [song.to_sim_dict(request) for song in songs if song.visible]

        return JsonResponse({'success': True, 'message': '搜索成功', 'data': data}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 搜索歌单
@csrf_exempt
@require_http_methods(["GET"])
def search_songlists(request):
    try:
        keyword = request.GET.get('keyword', '')
        num = request.GET.get('num', '')

        # 动态构建查询条件
        query = Q()

        if keyword:
            # 使用jieba对关键词进行分词
            keywords = list(set(jieba.cut_for_search(keyword)))
            if ' ' in keywords:
                keywords.remove(' ')

            for kw in keywords:
                query |= Q(title__icontains=kw)

        fields = {
            'tag_theme': 'tag_theme',
            'tag_scene': 'tag_scene',
            'tag_mood': 'tag_mood',
            'tag_style': 'tag_style',
            'tag_language': 'tag_language',
            'owner': 'owner__username'
        }
        # 从请求参数中获取查询字段
        for field, field_name in fields.items():
            value = request.GET.get(field)
            if value:
                query &= Q(**{f"{field_name}__icontains": value})

        # 查询歌单
        songLists = SongList.objects.filter(query)

        if num:
            songLists = songLists[:int(num)]

        # 将查询结果转换为字典格式
        data = [songList.to_sim_dict(request) for songList in songLists if songList.visible]

        return JsonResponse({'success': True, 'message': '搜索成功', 'data': data}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 搜索用户
@csrf_exempt
@require_http_methods(["GET"])
def search_users(request):
    try:
        keyword = request.GET.get('keyword', '')
        num = request.GET.get('num', '')

        # 动态构建查询条件
        query = Q()

        if keyword:
            # 使用jieba对关键词进行分词
            keywords = list(set(jieba.cut_for_search(keyword)))
            if ' ' in keywords:
                keywords.remove(' ')

            for kw in keywords:
                query |= Q(username__icontains=kw)

        # 查询用户
        users = User.objects.filter(query)

        if num:
            users = users[:int(num)]

        # 将查询结果转换为字典格式
        data = [user.to_pub_dict(request) for user in users]

        return JsonResponse({'success': True, 'message': '搜索成功', 'data': data}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
