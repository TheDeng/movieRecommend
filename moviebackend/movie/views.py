from django.http import JsonResponse
from movie.models import Movie,rating
from django.core.paginator import Paginator
from django.core.serializers import serialize
import json
from  collections import  Counter
from movie.tokenauth import tokenauth
import time
#通过电影名查询电影
def list_view(request):
    movie_name = request.GET.get('movie_name','')
    if not movie_name:
        result = {'code': 1, 'msg': '参数无效', 'data': ''}
        return JsonResponse(result)
    movie_list = Movie.objects.filter(name__icontains=movie_name)
    movie_list_s = serialize('json',movie_list)
    result = {'code': 0, 'msg': '请求成功', 'data': {'movie_list':movie_list_s}}
    return JsonResponse(result)

#通过标签分类去查询电影
def listbytag_view(request):
    target_st = request.GET.get('tags','')
    pagenum = request.GET.get('page','')
    size = request.GET.get('size','')
    print(target_st,pagenum,size)
    if not all((target_st,pagenum,size)):
        print("code1")
        result = {'code': 1, 'msg': '参数无效', 'data': ''}
        return JsonResponse(result)
    movie_list = Movie.objects.filter(tags__contains=target_st)#包含查询
    paginator = Paginator(movie_list,12)#Django分页
    page = paginator.page(pagenum)
    movie_list = list(page)
    movie_list_s = serialize('json',movie_list)
    json_data = json.loads(movie_list_s)
    print(json_data)
    result = {'code': 0, 'msg': '请求成功', 'data':json_data}
    return JsonResponse(result,safe=False)


def info_view(request):
    movie_id = request.GET.get('movieId','')
    print(movie_id)
    if not movie_id:

        result = {'code': 1, 'msg': '参数无效', 'data': ''}
        return JsonResponse(result)
    movie = Movie.objects.filter(movie_id=movie_id)

    if not movie:
        result = {'code': 1, 'msg': '不存在的电影id', 'data': ''}
        return JsonResponse(result)
    movie_s = serialize('json', movie)
    json_data = json.loads(movie_s)
    json_data =json_data[0]

    print(json_data)
    result = {'code': 0, 'msg': '请求成功', 'data': json_data }
    print(result)
    return JsonResponse(result,safe=False)


def update_view(request):
    user_md5 = request.GET.get('user_md5','')
    movie_id = request.GET.get('movie_id','')
    rating_num = request.GET.get('rating','')
    movie = Movie.objects.get(movie_id=movie_id)
    movie.score = (movie.score*movie.votes+float(rating_num))/(movie.votes+1)
    movie.score=round(movie.score, 2)
    movie.votes = movie.votes + 1
    movie.save()
    print(rating_num)
    if not all((user_md5,movie_id,rating_num)):
        result = {'code': 1, 'msg': '参数无效1', 'data': ''}
        return JsonResponse(result)
    if 0 <= float(rating_num) <= 5:

        str_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        rating_num = round(float(rating_num))
        rating.objects.create(user_md5=user_md5,movie_id=movie_id,rating=rating_num,time=str_time)

        result = {'code': 0, 'msg': '提交成功', 'data': ''}
        return JsonResponse(result)
    result = {'code': 1, 'msg': '参数错误', 'data': ''}
    return JsonResponse(result)


def hign_view(request):
    # if request.method == 'GET':
    #     result = {'code': 1, 'msg': '请求方式错误', 'data': ''}
    #     return JsonResponse(result)
    movie_list = Movie.objects.filter().order_by('-score')[:15]#查询分数排名前十的电影推荐
    movie_list_s = serialize('json',movie_list)
    json_data = json.loads(movie_list_s)
    print(json_data)
    result = {'code': 0, 'msg': '请求成功', 'data':json_data}
    print(result)
    return JsonResponse(result,safe=False)

#电影推荐算法
def recommend_view(request):
    # user_md5 = request.GET.get('user_pk','')
    user_md5 = request.GET.get('user_md5', '')
    print(user_md5)
    # print(request)
    # exit()
    if not user_md5:
        result = {'code': 1, 'msg': '参数错误', 'data': ''}
        print(result)
        return JsonResponse(result)
    # 这里为推荐算法
    # 算法思路：找出与用户打分类似的用户，然后通过协同过滤算法，利用相似性的比较，获取推荐的电影
    # 首先获取用户曾经打过分的电影
    movie_dict_list = list(rating.objects.filter(user_md5=user_md5).values('movie_id'))
    movie_list = []
    #计算评论电影的数量
    i = 0
    for movie in movie_dict_list:
        movie_list.append(movie['movie_id'])
        i+=1
    if i <= 4:
        result = {'code': 1, 'msg': '坪论的电影数量不够', 'data': ''}
        return JsonResponse(result)
    # 设定相似用户集合：
    same_user = []
    # 找到所有给当前用户打过分的电影也打过分的用户，全都放到same_user中
    for movie in movie_list:
        user_dict_list = list(rating.objects.filter(movie_id=movie).values('user_md5'))
        for user in user_dict_list:
            same_user.append(user['user_md5'])
    # 上面的用户中，有的用户可能跟当前用户打分重合部分很少，有的很多，需要进行排列
    # 用户相似性打分集合
    scores = {}
    for md5 in same_user:
        if md5 == user_md5:
            continue
        if md5 in scores.keys():
            old = scores[md5]
            scores[md5] = old + 1
        else:
            scores[md5] = 1
    target_user = []
    for s in sorted(scores.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        if len(target_user) < 10:
            target_user.append(s)
    # 存放结果
    result_list = []
    # 获取相似用户的所有电影打分列表
    for u in target_user:
        md5 = u[0]
        target_movie_dict_list = list(rating.objects.filter(user_md5=md5).values('movie_id'))
        for movie in target_movie_dict_list:
            result_list.append(movie['movie_id'])
    # 存放所有的电影id
    movies = []
    for m in result_list:
        movies.append(m)
    # 对电影列表进行统计，这里找到5个最值得被推荐的，数字可以自行更改
    result = Counter(movies).most_common(5)
    # 返回列表
    movie_list = []
    for r in result:
        movie_list.append(r[0])
    print(movie_list)
    json_data = []
    for movie_id in movie_list:
        movie = Movie.objects.filter(movie_id=movie_id)
        movie_s = serialize('json', movie)
        print(json.loads(movie_s))
        json_data .append(json.loads(movie_s)[0])
    print(json_data)
    result = {'code': 0, 'msg': '请求成功', 'data':json_data}
    return JsonResponse(result)