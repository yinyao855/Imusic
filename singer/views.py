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
    singer = Singer.objects.filter(singerID=singerid).first()
    if not singer:
        return JsonResponse({'success': False, 'message': '歌手不存在'}, status=404)
    for field in update_fields:
        field_value = data.get(field)
        if field_value is not None and field_value != '':
            setattr(singer, field, field_value)

    file_fields = {'singerImage': 'singerImage'}
    for field_name, field_attr in file_fields.items():
        uploaded_file = request.FILES.get(field_name)
        if uploaded_file:  # 如果有文件被上传
            # 删除原有文件
            original_file = getattr(singer, field_attr)
            if original_file:
                file_path = os.path.join(settings.MEDIA_ROOT, str(original_file))
                try:
                    os.remove(file_path)
                except FileNotFoundError:
                    pass  # 文件不存在，无需处理
            setattr(singer, field_attr, uploaded_file)

    singer.save()

    return JsonResponse({'success': True, 'message': '更新成功'}, status=200)


@csrf_exempt
@require_http_methods(["GET"])
def singer_get_songs(request, singerid):
    singer = Singer.objects.get(singerID=singerid)
    singer_info = singer.to_dict(request)
    return JsonResponse({'success': True, 'message': '获取歌手信息成功', 'data': singer_info}, status=200)
