# middleware.py

from django.conf import settings
from django.http import JsonResponse
import jwt


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 检查请求头中是否包含Authorization字段
        if 'Authorization' not in request.headers:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)

        # 获取token
        auth_header = request.headers['Authorization']
        token = auth_header.split(' ')[1]

        try:
            # 验证token
            decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # 将解码后的payload存储到request中以便后续视图函数使用
            request.username = decoded_payload.get('username', None)
            request.token_verification_code = decoded_payload.get('verification_code', None)
            # print("Username:", request.username)
            # print("Token Verification Code:", request.token_verification_code)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        response = self.get_response(request)
        return response
