from movie.models import User
from django.http import JsonResponse
import time
from django.shortcuts import HttpResponse

#登陆装饰器
def tokenauth(func):
    def auth(request,*args,**kwargs):
        token = request.META.get('HTTP_TOKEN','')
        if token:
            try:
                user = User.objects.get(user_md5=token)
            except User.DoesNotExist:
                result = {'code': 1, 'msg': '无效的token', 'data': ''}
                jsonresponse = JsonResponse(result)
                jsonresponse.status_code = 401
                return jsonresponse
            if int(user.updatetime-time.time) > 60*30:
                result = {'code': 1, 'msg': 'token已过期', 'data': ''}
                jsonresponse = JsonResponse(result)
                jsonresponse.status_code = 401
                return JsonResponse
            user.objects.update(updatetime=time.time())
            func(request,*args,**kwargs)
        result = {'code': 1, 'msg': '无效token', 'data': ''}
        jsonresponse = JsonResponse(result)
        jsonresponse.status_code = 401
        print(jsonresponse.content)
        print(jsonresponse)
        return jsonresponse
    return auth