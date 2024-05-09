from collections import defaultdict

from django.db.models import Count

from feature.models import Recent


# 生成用户听歌周报
def generate_user_weekly_report(user, start_date, end_date):
    # 获取用户听歌记录
    records = Recent.objects.filter(user=user, last_play__gte=start_date, last_play__lt=end_date)
    # 与歌曲信息关联
    songs = [record.song for record in records]
    # print(songs)
    # 与歌曲信息关联并获取听歌次数和时长
    times = 0
    duration = 0
    for record in records:
        times += int(record.play_count)
        duration += int(record.play_count) * float(record.song.duration)
    duration = int(duration)
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
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
    # 获取喜欢歌曲风格
    tag_dict = defaultdict(int)
    for song in songs:
        tag_dict[song.tag_theme] += 1
        tag_dict[song.tag_scene] += 1
        tag_dict[song.tag_mood] += 1
        tag_dict[song.tag_style] += 1
        tag_dict[song.tag_language] += 1
    # 去掉空tag
    tag_dict = {k: v for k, v in tag_dict.items() if k}
    # 排序tag_dict
    tag_dict = dict(sorted(tag_dict.items(), key=lambda x: x[1], reverse=True))
    # 选取前三个tag
    most_tag = list(tag_dict.keys())[:3]

    # 生成周报
    content = f"您在{start_date}至{end_date}这段时间内，共听歌{times}首，累计听歌时长{hours}小时{minutes}分钟{seconds}秒。" \
              f"您最常听的歌曲是{most_played_song.title}，共播放{most_played.play_count}次。" \
              f"您最常听的歌手是{singer_name}，共听过他/她的{len(most_played_artist_songs)}首歌曲，" \
              f"分别是{', '.join(song.title for song in most_played_artist_songs)}。" \
              f"您喜欢听的歌曲风格为{', '.join(most_tag)}。" \
              f"祝您生活愉快！"

    # 返回周报数据
    return {
        'username': user.username,
        'title': f"{start_date}至{end_date}听歌周报",
        'content': content
    }

# 生成用户上传周报
