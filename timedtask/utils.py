from collections import defaultdict

from django.db.models import Count

from feature.models import Recent
from message.models import Message
from song.models import Song
from songlist.models import SongList


# 生成用户听歌周报
def generate_user_weekly_report(user, start_date, end_date):
    # 获取用户听歌记录
    records = Recent.objects.filter(user=user, last_play__gte=start_date, last_play__lt=end_date)
    # 如果没有听歌记录，返回空
    if not records:
        content = f"您在{start_date}至{end_date}这段时间内没有听歌记录。"
        return {
            'username': user.username,
            'title': f"{start_date}至{end_date}听歌周报",
            'content': content
        }
    # 与歌曲信息关联
    songs = [record.song for record in records]
    # print(songs)
    # 与歌曲信息关联并获取听歌次数和时长
    times = 0
    duration = 0
    for record in records:
        times += int(record.w_play_count)
        duration += int(record.w_play_count) * float(record.song.duration)
    duration = int(duration)
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    # 最常听的歌曲
    most_played = max(records, key=lambda record: record.w_play_count)
    most_played_song = most_played.song
    # 最常听的歌手
    # 获取每个歌手的歌曲数量
    song_w_play_counts = records.values('song__singer').annotate(total_w_play_count=Count('id'))
    # 找到歌曲数量最多的歌手
    most_played_artist = max(song_w_play_counts, key=lambda x: x['total_w_play_count'])
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
              f"您最常听的歌曲是{most_played_song.title}，共播放{most_played.w_play_count}次。" \
              f"您最常听的歌手是{singer_name}，共听过他/她的{len(most_played_artist_songs)}首歌曲，" \
              f"分别是{', '.join(song.title for song in most_played_artist_songs)}。" \
              f"您喜欢听的歌曲风格为{', '.join(most_tag)}。" \
              f"祝您生活愉快！"

    # 生成周报消息
    message = Message(sender=None, receiver=user, title="听歌周报", content=content, type=1)
    message.save()

    # 返回周报数据
    return {
        'username': user.username,
        'title': f"{start_date}至{end_date}听歌周报",
        'content': content
    }


# 生成用户创作周报
def generate_user_upload_weekly_report(user, start_date, end_date):
    # 获取用户上传记录
    song_records = Song.objects.filter(uploader=user, visible=True, upload_date__gte=start_date, upload_date__lt=end_date)
    songlists_records = SongList.objects.filter(owner=user, visible=True, created_date__gte=start_date, created_date__lt=end_date)
    # 如果没有上传记录，返回空
    if not song_records and not songlists_records:
        content = f"您在{start_date}至{end_date}这段时间内没有创作记录。"
        return {
            'username': user.username,
            'title': f"{start_date}至{end_date}创作周报",
            'content': content
        }
    # 统计数量
    song_count = song_records.count()
    songlist_count = songlists_records.count()
    # 歌曲喜欢数和歌单收藏数
    like_count = 0
    for song in song_records:
        like_count += song.like
    collect_count = 0
    for songlist in songlists_records:
        collect_count += songlist.like
    # 生成周报
    content = f"您在{start_date}至{end_date}这段时间内，共上传歌曲{song_count}首，创建歌单{songlist_count}个。" \
              f"您上传的歌曲有{', '.join(song.title for song in song_records)}。" \
              f"您创建的歌单有{', '.join(songlist.title for songlist in songlists_records)}。" \
              f"您上传的歌曲共获得{like_count}个喜欢，创建的歌单共获得{collect_count}个收藏。" \
              f"祝您创作愉快！"
    # 生成周报消息
    message = Message(sender=None, receiver=user, title="创作周报", content=content, type=1)
    message.save()
    # 返回周报数据
    return {
        'username': user.username,
        'title': f"{start_date}至{end_date}创作周报",
        'content': content
    }
