from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Comment
from user.models import User
from song.models import Song
import message.views


@csrf_exempt
@require_http_methods(["POST"])
def add_comment(request):
    try:
        username = request.username
        songID = request.POST.get('songID')
        content = request.POST.get('content')

        user = User.objects.get(username=username)
        song = Song.objects.get(id=songID)

        new_comment = Comment(user=user, song=song, content=content)
        new_comment.save()

        # 发送消息给歌曲的上传者
        message.views.send_message(sender_name=username, receiver_name=song.uploader,
                                   title='新的评论',
                                   content=f"{username}评论了你上传的歌曲《{song.title}》：{content}",
                                   m_type=2)

        return JsonResponse({'success': True,
                             'message': '评论成功'}, status=201)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_comment(request):
    try:
        comment_id = request.GET.get('commentID')
        comment = Comment.objects.get(id=comment_id)
        sender = comment.user
        if request.role != 'admin' and request.username != sender.username:
            return JsonResponse({'success': False, 'message': '没有权限删除'}, status=403)
        receiver = comment.song.uploader
        Message.objects.filter(sender=sender,
                               receiver=receiver,
                               content=f"{sender.username}评论了你上传的歌曲《{comment.song.title}》：{comment.content}") \
            .delete()
        comment.delete()
        return JsonResponse({'success': True, 'message': '评论删除成功'}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
