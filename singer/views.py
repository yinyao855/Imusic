import os

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from imusic import settings
from singer.models import Singer


# Create your views here.
@csrf_exempt
@require_http_methods(["POST"])
def singer_update(request, singerid):
    data = request.POST
    if request.role != 'admin':
        return JsonResponse({'success': False, 'message': '没有权限操作'}, status=403)

    update_fields = ['singerName']
    singer = Singer.objects.get(singerID=singerid)
    for field in update_fields:
        setattr(singer, field, data.get(field, getattr(singer, field)))

    # 更新文件字段
    file_fields = {'singerImage': 'singerImage'}
    for field_name, field_attr in file_fields.items():
        if field_name in request.FILES:
            # 删除原有文件
            if getattr(singer, field_attr):
                file_path = os.path.join(settings.MEDIA_ROOT, str(getattr(singer, field_attr)))
                try:
                    os.remove(file_path)
                except FileNotFoundError:
                    pass  # 文件不存在，继续执行后续代码
            setattr(singer, field_attr, request.FILES[field_name])

    singer.save()

    return JsonResponse({'success': True, 'message': '更新成功'}, status=200)


@csrf_exempt
@require_http_methods(["GET"])
def singer_get_songs(request, singerid):
    singer = Singer.objects.get(singerID=singerid)
    singer_info = singer.to_dict(request)
    return JsonResponse({'success': True, 'message': '获取歌手信息成功', 'data': singer_info}, status=200)
