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
from .models import HostCapacityApiCheckRecord
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


def _get_api_info(client, api_params={}):
    """
    从自助接入的API获取对应返回信息
    """
    api_params.update({'token': 'host_capacity'})
    res = client.earlybird_host_capacity.get_disk_usage(api_params)
    failed_flag = None if 'mounted' in api_params else []
    return res.get('data') if res.get('result') else failed_flag


def show_disk_api_page(request):
    """
    api磁盘分区容量查询页面
    """
    client = get_client_by_request(request)
    ip_list = _get_api_info(client)
    mounted_list = [] if len(ip_list) == 0 else _get_api_info(
        client, {'ip': ip_list[0]})
    return render(request, 'host_capacity/disk_api_page.html', {'ip_list': ip_list, 'mounted_list': mounted_list})


def update_mounted_list(request):
    """
    根据页面选中ip更新对应分区列表
    """
    ip = request.GET.get('ip', '')
    client = get_client_by_request(request)
    mounted_list = _get_api_info(client, {'ip': ip})
    return JsonResponse({'updated_mounted_list': mounted_list})


def get_disk_capacity_data(request):
    """
    通过api查询分区容量使用比例并将查询记录入库
    """
    ip = request.GET.get('ip', '')
    mounted = request.GET.get('mounted', '')
    client = get_client_by_request(request)
    disk_capacity = _get_api_info(client, {'ip': ip, 'mounted': mounted})
    if isinstance(disk_capacity, dict):
        HostCapacityApiCheckRecord.objects.create(ip=disk_capacity['ip'],
                                                  used_percent=disk_capacity['used_percent'],
                                                  mounted=disk_capacity['mounted'])
        return JsonResponse({'result': True, 'message': 'success'})
    return JsonResponse({'result': False, 'message': 'ip and mounted params needed'})


def get_check_history(request):
    """
    获取api查询历史
    """
    check_records = HostCapacityApiCheckRecord.objects.order_by('-check_time')
    data = []
    for idx, _record in enumerate(check_records):
        data.append({
            'index': idx,
            'ip': _record.ip,
            'mounted': _record.mounted,
            'used_percent': _record.used_percent,
            'check_time': _record.check_time.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'result': True, 'data': data})


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
