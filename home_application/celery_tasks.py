# -*- coding: utf-8 -*-
from celery import task
from celery.task import periodic_task

import logging
import datetime
import time
import re
import base64
from blueapps.account.models import User
from blueking.component.shortcuts import get_client_by_user

logger = logging.getLogger('celery')

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

@task()
def get_capacity_task():
    """
    定义一个获取磁盘使用率异步任务
    """
    fast_execute_script_result = fast_execute_script(
        client, script_content, script_param, ip)
    # 如果快速脚本调用成功，执行log日志查询，获取执行内容
    if fast_execute_script_result['message'] == 'success':
        job_instance_id = fast_execute_script_result['data']['job_instance_id']
        get_job_instance_log_result = get_job_instance_log(
            client, job_instance_id)

        # 如果日志查询成功，提取内容
        if get_job_instance_log_result['message'] == 'success':
            # 匹配log_content规则
            regex = r"(?&lt;='log_content': ').*?(?=')"

            return re.findall(regex, str(get_job_instance_log_result), re.MULTILINE)
        else:
            return None


@periodic_task(run_every=datetime.timedelta(seconds=1))
def get_disk_periodic():
    """
    获取磁盘使用率周期执行定义
    """
    get_capacity_task.delay()