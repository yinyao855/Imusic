# middleware.py

from django.conf import settings
from django.http import JsonResponse
import jwt

exclude_path = [
    # 静态资源
    '/media',
    # 用户表
    '/users/login',
    # '/users/register',
    '/users/send-code',
    '/users/alldata',
    # 歌单表
    '/songlists/alldata',
    '/songlists/initdata',
    '/songlists/info',
    # 歌曲表
    '/songs/alldata',
    '/songs/info',
    '/songs/search',
    # 推荐表
    '/recommend/latest',
]


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 检查请求路径是否在排除列表中
        if any(request.path.startswith(path) for path in exclude_path):
            return self.get_response(request)

        # 检查请求头中是否包含Authorization字段
        if 'Authorization' not in request.headers:
            return JsonResponse({'success': False, 'message': 'Authorization header missing'}, status=401)

        # 获取token
        auth_header = request.headers['Authorization']
        token = auth_header.split(' ')[1]

        try:
            # 验证token
            decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # 将解码后的payload存储到request中以便后续视图函数使用
            request.username = decoded_payload.get('username', None)
            request.token_verification_code = decoded_payload.get('verification_code', None)
            request.role = decoded_payload.get('role', None)
            # print("Username:", request.username)
            # print("Token Verification Code:", request.token_verification_code)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'success': False, 'message': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'success': False, 'message': 'Invalid token'}, status=401)

        response = self.get_response(request)
        return response
