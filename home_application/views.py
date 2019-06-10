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

import logging
import datetime
import time
import re
import base64
from blueapps.account.models import User
from blueking.component.shortcuts import get_client_by_user

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
                host=host_name, ip=host_ip, df=host_df, note=host_note)
        except Exception as e:
            return json_ouput({'code': -1, 'msg': 'data insert faild.'})

        return json_ouput({'code': 0, 'msg': 'data insert success.'})

    else:
        return json_ouput({'code': 0, 'items': Hostlist.objects.to_dict(),})
        

def hello4(request):
    """
    hello4
    """
    return render(request, 'home_application/hello4.html')


def base64_encode(string):
    """
    对字符串进行base64编码
    """
    return base64.b64encode(string).decode("utf-8")


user = User.objects.get(username=844716598)
client = get_client_by_user(user.username)  # 这里是周期任务，不能通过request请求client

script_content = base64_encode(b"df -h ${1} | awk '{if(+$5&gt;0) print +$5}'")
script_param = base64_encode(b'/')
ip = '10.0.1.80'


def fast_execute_script(client, script_content, script_param, ip):
    """
    快速执行脚本函数
    """
    kwargs = {
        'bk_biz_id': 4
    }
    return client.job.fast_execute_script(kwargs)


def get_job_instance_log(client, job_instance_id):
    """
    对作业执行具体日志查询函数
    """

    kwargs = {
        'bk_biz_id': 4
    }
    time.sleep(2)  # todo 延时2s, 快速执行脚本需要一定的时间， 后期可以用celery串行两个函数
    return client.job.get_job_instance_log(kwargs)


def get_execute_log(request):
    fast_execute_script_result = fast_execute_script(client, script_content, script_param, ip)
    # 如果快速脚本调用成功，执行log日志查询，获取执行内容
    if fast_execute_script_result['message'] == 'success':
        job_instance_id = fast_execute_script_result['data']['job_instance_id']
        get_job_instance_log_result = get_job_instance_log(client, job_instance_id)

        # 如果日志查询成功，提取内容
        if get_job_instance_log_result['message'] == 'success':
            # 匹配log_content规则
            regex = r"(?&lt;='log_content': ').*?(?=')"

            return re.findall(regex, str(get_job_instance_log_result), re.MULTILINE)
        else:
            return None

def model_data_format(usages):
    usage_add_time = []
    usage_value = []
    for usage in usages:
        usage_add_time.append(usage.add_time.strftime("%Y/%m/%d %H:%M:%S"))
        usage_value.append(usage.value)
    return usage_add_time, usage_value


hosts = '10.0.1.80'
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


def model_data_format(usages):
    usage_add_time = []
    usage_value = []
    for usage in usages:
        usage_add_time.append(usage.add_time.strftime("%Y/%m/%d %H:%M:%S"))
        usage_value.append(usage.value)
    return usage_add_time, usage_value


def get_hosts(request):
    """
    hosts
    """
    # logger.error(u'logtest')
    if request.method == 'POST':
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
        return json_ouput({'code': 0, 'items': Hostlist.objects.to_dict(res_dict.ip), })

def hello5(request):
    """
    hello5
    """
    return render(request, 'home_application/hello5.html')


def hello6(request):
    """
    hello6
    """
    return render(request, 'home_application/hello4.html')
