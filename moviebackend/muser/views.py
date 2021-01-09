from django.shortcuts import render

# Create your views here.
import random,time

from django.shortcuts import render
from django.http import JsonResponse
from movie.models import User
import datetime
from movie.tokenauth import tokenauth
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import json
from movie.tokenauth import tokenauth
from django.core.handlers.wsgi import WSGIRequest

def test(request):
    print(type(request))   # 打印出request的类型
    print(request.environ)   # 打印出request的header详细信息
    # 循环打印出每一个键值对
    for k, v in request.environ.items():
        print(k, v)

def make_token():
    token_s = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    token = random.sample(token_s, 32)
    random.shuffle(token)
    token = ''.join(token)
    return token


def login_view(request):
    username = request.GET.get('username','')
    password = request.GET.get('password','')
    if not all((username,password)):
        result = {'code':1,'msg':'字段填写不完整','data':''}
        return JsonResponse(result)
    try:
        user = User.objects.filter(user_nickname=username,password=password)
    except User.DoesNotExist:
        result = {'code': 1, 'msg': '用户名或密码错误', 'data': ''}
        return JsonResponse(result)
    for i in range(len(user)):
        token = make_token()
        # user.update(token=token)
        user[i].token = token
        user[i].save()
    user = serialize('json', user)

    user= json.loads(user)
    user = user[0]
    print(user)


    # user_md5 = user[0].user_md5
    #
    #
    # user_name = user[0].user_nickname
    # user_name = serialize('json', user_name)
    # user_name = json.loads(user_name)
    result = {'code':0,'msg':'登陆成功','data':user}
    print(result)
    return JsonResponse(result,safe=False)


@tokenauth
def login_out_view(request):
    print("dddddddddd")
    result = {'code': 0, 'msg': '注销成功', 'data': ''}
    token = request.META.get('HTTP_TOKEN','')
    print(token)
    try:
        user = User.objects.get(token=token)
    except User.DoesNotExist:
        return result
    user.token = 0
    user.save()
    return result

@csrf_exempt
def register_view(request):
    # print(type(request))  # 打印出request的类型
    # print(request.environ)  # 打印出request的header详细信息
    # 循环打印出每一个键值对

    username = request.GET.get('username','')
    password = request.GET.get('password','')
    print(username)
    if not username and password:
        result = {'code': 1, 'msg': '字段填写不完整', 'data': ''}
        return JsonResponse(result)
    try:
        User.objects.get(user_nickname=username)
    except User.DoesNotExist:
        timenow = time.time()
        user_md5 = make_token()
        User.objects.create(user_nickname=username,password=password,updatetime=timenow,user_md5=user_md5)
        result = {'code': 0, 'msg': '注册成功', 'data': ''}
        return JsonResponse(result)
    result = {'code': 1, 'msg': '用户名已存在', 'data': ''}
    return JsonResponse(result)


