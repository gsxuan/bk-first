# coding:utf-8

from django.http import JsonResponse

from blueapps.utils.logger import logger
from blueapps.account.decorators import login_exempt
from get_capacity.models import HostCapacity


@login_exempt
def get_capacity_api(request):
    ip = request.GET.get('ip')
    disk = request.GET.get('mounted')
    # os = request.GET.get('os')

    if ip and disk:  # 查找最新磁盘容量记录
        disk_data = HostCapacity.objects.get_disk_data_based_on_ip(ip, disk)
        if disk_data is None:
            return JsonResponse({'result': False, 'message': 'get disk data failed.'})
        return JsonResponse({'result': True, 'message': 'get disk data success', 'data': disk_data})
    elif ip is None:  # 查询ip列表
        ip_list = HostCapacity.objects.get_ip_list()
        return JsonResponse({'result': True, 'message': 'ip list', 'data': ip_list})
    else:  # 查询某ip下分区列表
        disk_list = HostCapacity.objects.get_disk_list_based_on_ip(ip)
        return JsonResponse({'result': True, 'message': 'disk list', 'data': disk_list})


