# coding:utf-8

from django.http import JsonResponse

from blueapps.utils.logger import logger
from blueapps.account.decorators import login_exempt
from home_application.models import HostCapacity


@login_exempt
def get_capacity_api(request):
    """
    特定磁盘分区占用率前端格式数据获取
    """
    # disk = request.GET.get('disk', '')
    disk = '/dev'
    disk_data = HostCapacity.objects.get_disk_data(disk)

    time_list = []
    used_percent_list = []
    for _data in disk_data:
        time_list.append(_data.create_time.strftime('%Y-%m-%d %H:%M:%S'))
        used_percent_list.append(float(_data.used_percent[:-1]))

    res = {
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


