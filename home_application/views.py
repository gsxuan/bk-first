# -*- coding: utf-8 -*-
from django.shortcuts import render
# from blueapps.account.decorators import login_exempt
from django.views.decorators.csrf import csrf_exempt
# from common.log import logger
import json

from django.http import HttpResponse
from django.http.response import JsonResponse
from .models import HostModelManager
from .models import Hostlist

from .models import HostCapacity
from blueking.component.shortcuts import get_client_by_request





# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt 
#作业一
def home(request):
    """
    首页
    """
    return render(request, 'home_application/home.html')

#作业二
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

#作业三
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
                host=host_name, ip=host_ip, df=host_df, note=host_note)
        except Exception as e:
            return json_ouput({'code': -1, 'msg': 'data insert faild.'})

        return json_ouput({'code': 0, 'msg': 'data insert success.'})

    else:
        return json_ouput({'code': 0, 'items': Hostlist.objects.to_dict(),})
        
#作业四
def hello4(request):
    """
    hello4
    """
    options = HostCapacity.objects.get_disk_list()
    return render(request, 'home_application/hello4.html', context={'options': options})



def get_host_capacity_usage_data(request):
    """
    特定磁盘分区占用率前端格式数据获取
    """
    disk = request.GET.get('disk', '')
    disk_data = HostCapacity.objects.get_disk_data(disk)

    time_list = []
    used_percent_list = []
    for _data in disk_data:
        time_list.append(_data.create_time.strftime('%Y-%m-%d %H:%M:%S'))
        used_percent_list.append(float(_data.used_percent[:-1]))

    res = {
        'code': 0,
        'result': True,
        'message': 'success',
        'data': {
            'series': [{
                'name': 'disk: '+disk,
                'type': 'line',
                'data': used_percent_list,
            }],
            'xAxis': time_list,
        }
    }
    return JsonResponse(res)





#作业五
def hello5(request):
    """
    hello5
    """
    return render(request, 'home_application/hello4.html')

#作业六
def hello6(request):
    """
    hello6
    """
    return render(request, 'home_application/hello4.html')
