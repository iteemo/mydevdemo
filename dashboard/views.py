from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse,QueryDict
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
import json
from django.db import IntegrityError
from django.views import View
import logging
logger = logging.getLogger(__name__)



def index(request):
    # print(request.encoding)
    # print(request.META)
    # print(request.method)
    # print(request.body)
    # print(request.path)
    # res = HttpResponse()
    # res.content = "nihao"
    # res.status_code=888
    data = ["a", "b", "c"]
    dataa = {"a": "b", "c": ["d", "e", "f"]}
    # return HttpResponse(data)
    # print(request.GET)
    # print(request.GET.get("aa"))
    # print(request.GET.getlist("cc"))
    # return JsonResponse("")
    # return res
    # return HttpResponse("")
    if request.method == 'GET':
        print(request.path)
        data = request.GET.copy()
        print("aa=", request.GET.get('aa'))
        print("cc=", request.GET.getlist('cc'))
        print('body=', request.body)
    elif request.method == "POST":
        print(request.POST)
        # print(request.body)
    elif request.method == 'DELETE':
        print(request.path)

    return HttpResponse("")


# def login(request):
#     msg = ""
#     if request.method == "POST":
#         name = request.POST.get("username")
#         passwd = request.POST.get('password')
#         if name == "admin" and passwd == '123456':
#             msg = "登陆成功"
#             print(msg)
#         else:
#             msg = "denglyshibai"
#     else:
#         msg = '请求方法不被允许'
#
#     return HttpResponse(msg)

def loginview(request):
    # stat_id = 0
    countid = User.objects.all().count()
    userlist = []
    if request.method == "POST":
        stat_id = int(request.POST.get('stat_id'))
        stop_id = int(request.POST.get('stop_id'))
        userinfo = User.objects.all()[stat_id:stop_id]
        if stat_id > 0 and stop_id < countid:
            for i in userinfo:
                rest = {
                    'id': i.id,
                    'name': i.username,
                    'mail': i.email

                }
                userlist.append(rest)
            # return render(request,'aaa.html')
            # return JsonResponse(userlist, safe=False)
            return JsonResponse(userlist, safe=False)
    return render(request, 'login.html')


def article_detail(request, *args, **kwargs):
    return JsonResponse(kwargs)


class Indexview(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("index view")


def user(request, *args, **kwargs):
    if request.method == "GET":
        return HttpResponse("展示用户信息")
    elif request.method == "POST":
        return HttpResponse("验证用户信息")
    elif request.method == "PUT":
        return HttpResponse("修改用户信息")
    elif request.method == "DELETE":
        return HttpResponse("删除用户信息")
    return HttpResponse("")


# class Userview(View):
#     http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace', 'list', 'dict']
#
#     def get(self, request, *args, **kwargs):
#         page = int(request.GET.get("page")) - 1
#         start_id = int(page * 10)
#         stop_id = start_id + 10
#         queryset = User.objects.all()[start_id:stop_id]
#         data = [{"id": user.id, "mail:": user.email, "name": user.username} for user in queryset]
#         return JsonResponse(data, safe=False)
#
#     def post(self, request, *args, **kwargs):
#         return HttpResponse("验证用户信息")
#
#     def put(self, request, *args, **kwargs):
#         return HttpResponse("修改用户信息")
#
#     def delete(self, request, *args, **kwargs):
#         return HttpResponse("删除用户信息")
#
#     def list(self, request, *args, **kwargs):
#         return HttpResponse("展示用户列表")
#
#     def dict(self, request, *args, **kwargs):
#         return HttpResponse("展示用户zidian列表")


class Userview2(View):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace', 'list', 'dict']
    def list(self, request, *args, **kwargs):
        queryset = User.objects.all()
        # 每页显示10条,当少于5条的时候合并到上一页
        p = Paginator(queryset, 10, )
        # 获取页码
        page = request.GET.get("page")
        # 获取页码内容
        page = p.page(page)
        # object.list 第一分页对象的元素列表
        data = [{"id": user.id, "mail:": user.email, "name": user.username} for user in page.object_list]
        return JsonResponse(data, safe=False)

    def post(self, request, *args, **kwargs):
        logger.debug("创建用户")
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        # mail = request.POST.get("mail")
        data = request.POST.dict()
        print(data)
        # data={"name":name,"password":password,"mail":mail}
        # return JsonResponse(data)
        try:
            res = User.objects.create_user(**data)
        except IntegrityError:
            logger.debug("用户存在")
            return JsonResponse({"errmsg":"用户存在"})

        userdata = [{"id": res.id, "name": res.username}]
        return JsonResponse({"id": res.id, "name": res.username},safe=False)
    # def put(self,request,*args,**kwargs):
    #     res = User.objects.
    def get(self,request,*args,**kwargs):
        name = request.GET.get("username")
        try:
            res=User.objects.get(username=name)
        except:
            return JsonResponse({"errmsg": "用户bu存在"})
        print("---------------------->",res)
        userdata = [{ "name": res.username}]
        return JsonResponse({"id": res.id, "name": res.username}, safe=False)

    def delete(self,request,*args,**kwargs):
        name=request.GET.get("username")
        data = request.GET.dict()
        print(data)
        try:
            res=User.objects.get(**data)
        except User.DoesNotExist:
            logger.error({"errmsg": "{}用户bu存在".format(name)})
            return JsonResponse({"errmsg": "{}用户bu存在".format(name)})

        print(type(res))
        print(res)
        return JsonResponse({"name":"{},已删除".format(name)})
    def put(self,request,*args,**kwargs):
        # data = request.GET.dict()
        # data = request.POST.dict()
        data = QueryDict(request.body).dict()
        print(data)


        name = data.get('username')
        print(name)
        try:
            User.objects.filter(username=name).update(**data)
            try:
                res = User.objects.get(username=name)
            except User.DoesNotExist:
                logger.error({"errmsg": "{}用户bu存在".format(name)})
                return JsonResponse({"errmsg": "{}用户bu存在".format(name)})
        except:
            logger.error({"errmsg": "{}用户bu存在".format(name)})
            return JsonResponse({"errmsg": "{}用户bu存在".format(name)})


        return JsonResponse({"id": res.id, "name": res.username}, safe=False)