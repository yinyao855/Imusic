import os

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import User
from django.conf import settings


# Create your views here.
@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        # 获取用户提交的数据
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        avatar = request.FILES.get('avatar')
        bio = request.POST.get('bio')
        # 判断用户是否已经存在
        user = User.objects.filter(username=username)
        if user:
            return JsonResponse({'success': 0, 'message': '用户名已存在'})
        # 创建用户
        user = User(username=username, email=email,
                    password=password, avatar=avatar, bio=bio)
        user.save()
        return JsonResponse({'success': 1, 'message': '注册成功'})

    return JsonResponse({'success': 0, 'message': '注册失败，数据或请求方式错误'})


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        # 获取用户提交的数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 判断用户是否存在
        user = User.objects.filter(username=username, password=password).first()
        if user:
            avatar_url = None
            if user.avatar:
                # print(user.avatar.url)
                avatar_dir = os.path.join(settings.BASE_DIR, user.avatar.url)
                avatar_url = request.build_absolute_uri(avatar_dir)
            data = {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'bio': user.bio if user.bio else None,
                'avatar': avatar_url,
                'role': user.role,
                'registration_date': user.registration_date
            }
            return JsonResponse({'success': 1, 'message': '登录成功', 'data': data})
        return JsonResponse({'success': 0, 'message': '用户名或密码错误'})

    return JsonResponse({'success': 0, 'message': '登录失败，数据或请求方式错误'})


# 获取用户信息
@csrf_exempt
def get_user_info(request, username):
    if request.method == 'GET':
        user = User.objects.filter(username=username).first()
        if user:
            avatar_url = None
            if user.avatar:
                # print(user.avatar.url)
                avatar_dir = os.path.join(settings.BASE_DIR, user.avatar.url)
                avatar_url = request.build_absolute_uri(avatar_dir)
            data = {
                'username': user.username,
                'email': user.email,
                'bio': user.bio if user.bio else None,
                'avatar': avatar_url,
                'role': user.role,
                'registration_date': user.registration_date
            }
            return JsonResponse({'success': 1, 'message': '获取用户信息成功', 'data': data})
        return JsonResponse({'success': 0, 'message': '用户不存在'})

    return JsonResponse({'success': 0, 'message': '获取用户信息失败，数据或请求方式错误'})


# 修改用户信息
@csrf_exempt
def update_user_info(request, username):
    if request.method == 'POST':
        # 获取用户提交的数据
        email = request.POST.get('email')
        avatar = request.FILES.get('avatar')
        bio = request.POST.get('bio')
        # 判断用户是否存在
        user = User.objects.filter(username=username).first()
        if user:
            user.email = email
            user.avatar = avatar
            user.bio = bio
            user.save()
            return JsonResponse({'success': 1, 'message': '用户信息修改成功'})
        return JsonResponse({'success': 0, 'message': '用户不存在'})

    return JsonResponse({'success': 0, 'message': '用户信息修改失败，数据或请求方式错误'})


# 删除用户，测试用
@csrf_exempt
def delete_user(request, username):
    if request.method == 'DELETE':
        # 判断用户是否存在
        user = User.objects.filter(username=username).first()
        if user:
            user.delete()
            return JsonResponse({'success': 1, 'message': '用户删除成功'})
        return JsonResponse({'success': 0, 'message': '用户不存在'})

    return JsonResponse({'success': 0, 'message': '用户删除失败，数据或请求方式错误'})


# 获取所有用户信息，测试用
@csrf_exempt
def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        data = []
        for user in users:
            avatar_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, user.avatar.url)) if user.avatar else None
            user_data = {
                'username': user.username,
                'email': user.email,
                'bio': user.bio if user.bio else None,
                'avatar': avatar_url,
                'role': user.role,
                'registration_date': user.registration_date
            }
            data.append(user_data)
        return JsonResponse({'success': 1, 'message': '获取所有用户信息成功', 'data': data})

    return JsonResponse({'success': 0, 'message': '获取所有用户信息失败，数据或请求方式错误'})


# 更改用户权限
@csrf_exempt
def change_user_role(request):
    with open('authorized_key', 'r') as f:
        authorized_key = f.read().strip()
    print(authorized_key)
    if request.method == 'POST':
        # 获取用户提交的数据，都是用户名
        cur_user = request.POST.get('cur_user')
        dir_user = request.POST.get('dir_user')
        role = request.POST.get('role')
        key = request.POST.get('key')
        flag = 0
        user = User.objects.filter(username=cur_user).first()
        if key == authorized_key:
            flag = 1
        if user and user.role == 'admin':
            flag = 1
        if not flag:
            return JsonResponse({'success': 0, 'message': '用户权限修改失败，权限不足'})
        user = User.objects.filter(username=dir_user).first()
        if not user:
            return JsonResponse({'success': 0, 'message': '用户不存在'})
        if role not in ['admin', 'user']:
            return JsonResponse({'success': 0, 'message': '用户权限修改失败，权限错误'})
        user.role = role
        user.save()
        return JsonResponse({'success': 1, 'message': '用户权限修改成功'})

    return JsonResponse({'success': 0, 'message': '用户权限修改失败，数据或请求方式错误'})
