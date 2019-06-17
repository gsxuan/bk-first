# coding:utf-8

from django.shortcuts import render
from django.http import JsonResponse

from .models import HostCapacity, HostCapacityApiCheckRecord
from blueking.component.shortcuts import get_client_by_request


def show_get_capacity_usage(request):
    """
    指定磁盘分区占用率查询
    """
    options = HostCapacity.objects.get_disk_list()
    return render(request, 'get_capacity/get_capacity_usage.html', context={'options': options})


def get_get_capacity_usage_data(request):
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
    api_params.update({'token': 'get_capacity'})
    res = client.earlybird_get_capacity.get_disk_usage(api_params)
    failed_flag = None if 'mounted' in api_params else []
    return res.get('data') if res.get('result') else failed_flag


def show_disk_api_page(request):
    """
    api磁盘分区容量查询页面
    """
    client = get_client_by_request(request)
    ip_list = _get_api_info(client)
    mounted_list = [] if len(ip_list) == 0 else _get_api_info(client, {'ip': ip_list[0]})
    return render(request, 'get_capacity/disk_api_page.html', {'ip_list': ip_list, 'mounted_list': mounted_list})


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

