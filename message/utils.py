from django.db.models import Sum, Count, ExpressionWrapper, F, DurationField
from django.forms import IntegerField

from feature.models import Recent
from user.models import User


# 生成用户听歌周报
def generate_user_weekly_report(user, start_date, end_date, request):
    # 获取用户听歌记录
    records = Recent.objects.filter(user=user, last_play__gte=start_date, last_play__lt=end_date)
    # 与歌曲信息关联
    songs = [record.song for record in records]
    # 与歌曲信息关联并获取听歌次数和时长
    times = 0
    duration = 0
    for record in records:
        times += int(record.play_count)
        duration += int(record.play_count) * float(record.song.duration)
    duration = int(duration)
    # 最常听的歌曲
    most_played = max(records, key=lambda record: record.play_count)
    most_played_song = most_played.song
    # 最常听的歌手
    # 获取每个歌手的歌曲数量
    song_play_counts = records.values('song__singer').annotate(total_play_count=Count('id'))
    # 找到歌曲数量最多的歌手
    most_played_artist = max(song_play_counts, key=lambda x: x['total_play_count'])
    singer_name = most_played_artist['song__singer']
    # 获取歌手歌曲信息
    most_played_artist_songs = [song for song in songs if song.singer == singer_name]
    # 获取歌曲风格
    # most_tag_theme = max(songs, key=lambda song: song.tag_theme)

    # 返回周报数据
    return {
        'username': user.username,
        'times': times,
        'duration': duration,
        'most_played_song': most_played_song.to_dict(request),
        'most_played_count': most_played.play_count,
        'most_played_artist': singer_name,
        'most_played_artist_songs': [song.to_dict(request) for song in most_played_artist_songs]
    }

