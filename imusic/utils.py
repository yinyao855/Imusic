import jwt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from imusic.settings import SECRET_KEY


# 检查token是否过期
@csrf_exempt
@require_http_methods(["GET"])
def check_token(request):
    # 检查请求头中是否包含Authorization字段
    if 'Authorization' not in request.headers:
        return JsonResponse({'success': False, 'message': 'Authorization header missing'}, status=200)

    # 获取token
    auth_header = request.headers['Authorization']
    token = auth_header.split(' ')[1]
    try:
        # 验证token
        jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return JsonResponse({'success': True, 'message': 'Token valid'}, status=200)
    except jwt.ExpiredSignatureError:
        return JsonResponse({'success': False, 'message': 'Token expired'}, status=200)
    except jwt.InvalidTokenError:
        return JsonResponse({'success': False, 'message': 'Invalid token'}, status=200)
