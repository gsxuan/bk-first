# -*- coding: utf-8 -*-
from django.shortcuts import render


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """
    return render(request, 'home_application/home.html')

def hello(request):
    """
    hello
    """
    return render(request, 'home_application/hello.html')

def hello(request):
    """
    hello2
    """
    return render(request, 'home_application/hello2.html')
    
# 自己提取的一个工具函数
def render_json(res_dict):
    return HttpResponse(json.dumps(res_dict), content_type='application/json')

# 输入值提交请求
def say_hello(request):
    data = request.POST.get('input', None)
    data = 'Congratulations!' if data == 'Hello Blueking' else 'Try input Hello Blueking'
    res = {'data': data}
    return render_json(res)
