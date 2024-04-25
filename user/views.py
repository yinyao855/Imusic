import os

from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import User
from songlist.models import SongList
from django.conf import settings
from django.db import transaction


# Create your views here.
@csrf_exempt
@require_http_methods(["POST"])
def user_register(request):
    # 获取用户提交的数据
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    avatar = request.FILES.get('avatar')
    bio = request.POST.get('bio')

    required_fields = ['username', 'password']
    for field in required_fields:
        if not request.POST.get(field):
            return JsonResponse({'success': False, 'message': f'缺少字段：{field}'}, status=400)
    # 判断用户是否已经存在
    user = User.objects.filter(username=username).first()
    if user:
        return JsonResponse({'success': False, 'message': '用户名已存在'}, status=400)
    # 创建用户
    with transaction.atomic():
        user = User(username=username, email=email,
                    password=password, avatar=avatar, bio=bio)
        user.full_clean()
        user.save()

    return JsonResponse({'success': True, 'message': '注册成功'}, status=201)


@csrf_exempt
@require_http_methods(["POST"])
def user_login(request):
    # 获取用户提交的数据
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 判断用户是否存在
    user = User.objects.filter(username=username, password=password).first()
    if user:
        data = user.to_dict(request)
        return JsonResponse({'success': True, 'message': '登录成功', 'data': data}, status=200)
    return JsonResponse({'success': False, 'message': '用户名或密码错误'}, status=400)


# 获取用户信息
@csrf_exempt
@require_http_methods(["GET"])
def get_user_info(request, username):
    user = User.objects.filter(username=username).first()
    if user:
        data = user.to_dict(request)
        return JsonResponse({'success': True, 'message': '获取用户信息成功', 'data': data}, status=200)
    return JsonResponse({'success': False, 'message': '用户不存在'}, status=400)


# 修改用户信息
@csrf_exempt
@require_http_methods(["POST"])
def update_user_info(request, username):
    # 判断用户是否存在
    try:
        user = User.objects.filter(username=username).first()
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=400)

    try:
        data = request.POST

        update_fields = ['email', 'bio']
        for field in update_fields:
            if data.get(field):
                setattr(user, field, data[field])

        file_fields = {'avatar': 'avatar'}
        for field_name, field_attr in file_fields.items():
            if field_name in request.FILES:
                if getattr(user, field_attr):
                    file_path = os.path.join(settings.MEDIA_ROOT, str(getattr(user, field_attr)))
                    try:
                        os.remove(file_path)
                    except FileNotFoundError:
                        pass
                setattr(user, field_attr, request.FILES[field_name])

        with transaction.atomic():
            user.full_clean()
            user.save()
        return JsonResponse({'success': True, 'message': '用户信息修改成功'}, status=200)
    except ValidationError as e:
        return JsonResponse({'success': False, 'message': e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


# 删除用户，测试用
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user(request, username):
    # 判断用户是否存在
    user = User.objects.filter(username=username).first()
    if user:
        # 需要删除用户的头像文件
        if user.avatar:
            file_path = os.path.join(settings.MEDIA_ROOT, str(user.avatar))
            try:
                os.remove(file_path)
            except FileNotFoundError:
                pass
        user.delete()
        return JsonResponse({'success': True, 'message': '用户删除成功'}, status=200)
    return JsonResponse({'success': False, 'message': '用户不存在'}, status=400)


# 获取所有用户信息，测试用
@csrf_exempt
@require_http_methods(["GET"])
def get_all_users(request):
    users = User.objects.all()
    data = []
    for user in users:
        user_data = user.to_dict(request)
        data.append(user_data)
    return JsonResponse({'success': True, 'message': '获取所有用户信息成功', 'data': data}, status=200)


# 更改用户权限
@csrf_exempt
@require_http_methods(["POST"])
def change_user_role(request):
    with open('authorized_key', 'r') as f:
        authorized_key = f.read().strip()
    # print(authorized_key)

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
        return JsonResponse({'success': False, 'message': '用户权限修改失败，权限不足'}, status=400)
    user = User.objects.filter(username=dir_user).first()
    if not user:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=400)
    if role not in ['admin', 'user']:
        return JsonResponse({'success': False, 'message': '用户权限修改失败，权限错误'}, status=400)
    user.role = role
    user.save()
    return JsonResponse({'success': False, 'message': '用户权限修改成功'}, status=200)


# 修改密码
@csrf_exempt
@require_http_methods(["POST"])
def change_password(request):
    # 获取用户提交的数据
    username = request.POST.get('username')
    new_password = request.POST.get('new_password')
    # 判断用户是否存在
    user = User.objects.filter(username=username).first()
    if user:
        user.password = new_password
        user.save()
        return JsonResponse({'success': True, 'message': '密码修改成功'}, status=200)
    return JsonResponse({'success': False, 'message': '用户名不存在'}, status=400)


@require_http_methods(["GET"])
def get_user_songlists(request):
    user_id = request.GET.get('userid')
    if not user_id:
        return JsonResponse({'success': False, 'message': '缺少用户ID'}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'}, status=404)

    # 获取该用户的所有歌单
    user_songlists = SongList.objects.filter(owner=user)

    songlists_data = []
    for songlist in user_songlists:
        # 获取歌单中的所有歌曲
        songs_data = [{
            'songname': song.title,
            'songid': song.id,
            'singerid': song.singer.id if song.singer else None
        } for song in songlist.songs.all()]

        songlists_data.append({
            'songlist_name': songlist.title,
            'songs': songs_data
        })

    return JsonResponse({
        'success': True,
        'songlist': songlists_data
    })