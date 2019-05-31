# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from common.log import logger
from django.http import HttpResponse
from django.http.response import JsonResponse
from .models import HostModelManager
from .models import Hostlist
import json

# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """
    return render(request, 'home_application/home.html')

def hello2(request):
    """
    hello2
    """
    return render(request, 'home_application/hello2.html')

# json
def json_ouput(res):
    return HttpResponse(json.dumps(res), content_type='application/json')

# submit
def say_hello(request):
    data = request.POST.get('input', 'null')
    if data == 'Hello Blueking':
        data = 'Congratulations!' 
    else:
        data = 'input error'
    res = {'data': data}
    return json_ouput(res)


def hello3(request):
    """
    hello3
    """
    return render(request, 'home_application/hello3.html')

def host_data(request):
    """
    host_list
    """
    # logger.error(u'logtest')
    if request.method  == 'POST':
        host_name = request.POST.get('hostname', None)
        host_ip = request.POST.get('hostip', None)
        host_df = request.POST.get('hostdf', None)
        host_note = request.POST.get('hostnote', None)

        try:
            Hostlist.objects.create(
                name=host_name, ip=host_ip, df=host_df, note=host_note)
        except Exception as e:
            return json_ouput({'code': -1, 'msg': 'data insert faild.'})

        return json_ouput({'code': 0, 'msg': 'data insert success.'})

    else:
        return json_ouput({'code': 0, 'items': Hostlist.objects.to_dict(),
            # 'catalogues': {
            #     'host_name': '主机名',
            #     'host_ip': '主机ip',
            #     'host_df': '磁盘分区',
            #     'host_note': '备注',
            #     'host_createtime': '创建时间',
            # }
        })
        

