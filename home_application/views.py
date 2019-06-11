# -*- coding: utf-8 -*-
from django.shortcuts import render
# from blueapps.account.decorators import login_exempt
from django.views.decorators.csrf import csrf_exempt
# from common.log import logger
from django.http import HttpResponse
from django.http.response import JsonResponse
from .models import HostModelManager
from .models import Hostlist
import json




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
    return render(request, 'home_application/hello4.html')


def model_data_format(usages):
    usage_add_time = []
    usage_value = []
    for usage in usages:
        usage_add_time.append(usage.add_time.strftime("%Y/%m/%d %H:%M:%S"))
        usage_value.append(usage.value)
    return usage_add_time, usage_value


def api_disk_usage(request):
    """
    磁盘使用率API接口
    """
    data_list = []
    for _data in hosts:
        disk_usages = _data.DiskUsage.all()
        disk_usage_add_time, disk_usage_value = model_data_format(disk_usages)

        data_list.append(
            {
                'ip': _data.ip,
                'system': _data.system,
                'mounted': _data.disk,
                'disk_usage': {
                    "xAxis": disk_usage_add_time,
                    "series": [
                        {
                            "name": "磁盘使用率",
                            "type": "line",
                            "data": disk_usage_value
                        }
                    ]
                }
            }
        )

    return JsonResponse({
        "result": True,
        "data": data_list,
        "message": 'ok'
    })

#作业五
def hello5(request):
    """
    hello5
    """
    return render(request, 'home_application/hello5.html')

#作业六
def hello6(request):
    """
    hello6
    """
    return render(request, 'home_application/hello4.html')
