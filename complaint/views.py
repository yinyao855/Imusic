import re

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from message.views import send_message
from user.models import User
from song.models import Song
from songlist.models import SongList
from complaint.models import Complaint
from message.models import Message


@csrf_exempt
@require_http_methods(["POST"])
def complain(request):
    try:
        with transaction.atomic():
            username = request.username
            complainer = User.objects.get(username=username)
            complaint_content = request.POST.get('content')
            if request.path.startswith('/songs/'):
                object_type = 'song'
                object_id = request.POST.get('song_id')
                song = Song.objects.get(id=object_id)
                complained = song.uploader
                message_content = f'您上传的歌曲《{song.title}》被投诉，请等待管理员处理。'
            else:
                object_type = 'songlist'
                object_id = request.POST.get('songlist_id')
                songlist = SongList.objects.get(id=object_id)
                complained = songlist.owner
                message_content = f'您创建的歌单"{songlist.title}"被投诉，请等待管理员处理。'
            complaint = Complaint(
                complainer=complainer,
                complained=complained,
                content=complaint_content,
                object_type=object_type,
                object_id=object_id
            )
            # 记录在投诉表里
            complaint.save()
            # 通知管理员有投诉消息，消息内容就只记录个投诉表里的id吧
            send_message(title='投诉消息', content=f'{complaint.id}', message_type=6,
                         sender=None,
                         receiver=User.objects.get(username='yy'))
            # 官方给所有者发送消息
            send_message(title='投诉消息', content=message_content, message_type=6,
                         sender=User.objects.get(username='yy'),
                         receiver=complained)

        return JsonResponse({'success': True, 'message': '投诉成功'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '投诉者不存在'}, status=400)
    except Song.DoesNotExist:
        return JsonResponse({'success': False, 'message': '被投诉歌曲不存在'}, status=400)
    except SongList.DoesNotExist:
        return JsonResponse({'success': False, 'message': '被投诉歌单不存在'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_complaint(request):
    if request.role != 'admin':
        return JsonResponse({'success': False, 'message': '没有权限访问'}, status=403)
    try:
        complaint_id = request.GET.get('complaint_id')
        if not complaint_id:
            return JsonResponse({'success': False, 'message': '未传入complaint_id'}, status=400)
        complaint = Complaint.objects.get(id=complaint_id)
        return JsonResponse({'success': True, 'message': '获取投诉信息成功',
                             'data': complaint.to_dict(request)}, status=200)
    except Complaint.DoesNotExist:
        return JsonResponse({'success': False, 'message': '投诉记录不存在'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def handle_complaint(request):
    if request.role != 'admin':
        return JsonResponse({'success': False, 'message': '没有权限访问'}, status=403)
    try:
        complaint = Complaint.objects.get(id=request.POST.get('complaint_id'))
        is_remove = request.POST.get('is_remove')
        # reason里要说明是否下架以及理由
        reason = request.POST.get('reason')
        message_to_complained_content = reason
        # 如果管理员确定需要下架
        if is_remove:
            # 歌曲或者歌单
            complaint_object = Song.objects.get(id=complaint.object_id) \
                if complaint.object_type == 'song' \
                else SongList.objects.get(id=complaint.object_id)
            # 设置为不可见
            complaint_object.visible = False
            complaint_object.save()
            message_to_complained_content = str(complaint.id) + ' ' + message_to_complained_content
        complainer = complaint.complainer
        complained = complaint.complained
        # 向投诉者和被投诉者发送审查结果
        # 对于被投诉者，需要传递投诉信息的id，以便申诉，前端需要处理字符串获取投诉的id和理由
        send_message(title='审查结果',
                     content=message_to_complained_content,
                     message_type=6,
                     sender=User.objects.get(username='yy'),
                     receiver=complained)
        send_message(title='审查结果',
                     content=reason,
                     message_type=6,
                     sender=User.objects.get(username='yy'),
                     receiver=complainer)
        return JsonResponse({'success': True, 'message': ' 处理投诉成功'}, status=200)
    except Complaint.DoesNotExist:
        return JsonResponse({'success': False, 'message': '投诉记录不存在'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def appeal(request):
    try:
        complaint_id = request.POST.get('complaint_id')
        if request.username != Complaint.objects.get(id=complaint_id).complained.username:
            return JsonResponse({'success': False, 'message': '没有权限访问'}, status=403)
        reason = request.POST.get('reason')
        send_message(title='申诉',
                     content=complaint_id + ' ' + reason,
                     message_type=7,
                     sender=User.objects.get(username=request.username),
                     receiver=User.objects.get(username='yy'))
        return JsonResponse({'success': True, 'message': ' 申诉发送成功'}, status=200)
    except Complaint.DoesNotExist:
        return JsonResponse({'success': False, 'message': '投诉记录不存在'}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def get_appeal(request):
    if request.role != 'admin':
        return JsonResponse({'success': False, 'message': '没有权限访问'}, status=403)
    try:
        message_id = request.GET.get('message_id')
        if not message_id:
            return JsonResponse({'success': False, 'message': '未传入message_id'}, status=400)
        message = Message.objects.get(id=message_id)
        match = re.match(r"(\d+)\s(.+)", message.content)
        complaint_id = match.group(1)
        complaint = Complaint.objects.get(id=complaint_id)
        appeal_reason = match.group(2)
        # data里包括：之前的投诉（方便管理员回顾）和现在的申诉理由，日期
        data = {
            'complaint': complaint.to_dict(request),
            'reason': appeal_reason,
            'date': message.send_date,
        }
        return JsonResponse({'success': True, 'message': '获取申诉信息成功',
                             'data': data}, status=200)
    except Message.DoesNotExist:
        return JsonResponse({'success': False, 'message': '申诉消息记录不存在'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def handle_appeal(request):
    if request.role != 'admin':
        return JsonResponse({'success': False, 'message': '没有权限访问'}, status=403)
    try:
        complaint = Complaint.objects.get(id=request.POST.get('complaint_id'))
        is_recover = request.POST.get('is_recover')
        # 重新上架/维持下架状态的原因
        # 格式为"重新上架。原因是：..."
        reason = request.POST.get('reason')
        if is_recover:
            complaint_object = Song.objects.get(id=complaint.object_id) \
                if complaint.object_type == 'song' \
                else SongList.objects.get(id=complaint.object_id)
            complaint_object.visible = True
            complaint_object.save()
            send_message(title='申诉通知',
                         content='被投诉内容所有者在内容下架后选择申诉，经过管理人员再次考虑，决定重新上架。理由：'
                                 + reason,
                         message_type=7,
                         sender=User.objects.get(username='yy'),
                         receiver=complaint.complainer)
        send_message(title='申诉通知',
                     content=reason,
                     message_type=7,
                     sender=User.objects.get(username='yy'),
                     receiver=complaint.complained)
        return JsonResponse({'success': True, 'message': '处理申诉成功'}, status=200)
    except Complaint.DoesNotExist:
        return JsonResponse({'success': False, 'message': '投诉消息记录不存在'}, status=400)
