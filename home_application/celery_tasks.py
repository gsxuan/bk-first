# coding:utf-8
import base64
import logging
import datetime
from time import sleep

from celery.schedules import crontab
from celery import task
from celery.task import periodic_task

from .models import HostCapacity

from blueapps.account.models import User
from blueking.component.shortcuts import get_client_by_user

logger = logging.getLogger('celery')

def get_fast_execute_script_job_instance_id(client, script_kwargs):
    """
    调用快速执行脚本api并返回作业状态和实例id
    """
    res = client.job.fast_execute_script(**script_kwargs)
    job_instance_id = res.get('data').get(
        'job_instance_id') if res.get('result') is True else -1
    return res.get('result'), job_instance_id


def save_host_capacity_usage(client, ip,  log_kwargs):
    """
    读取快速执行脚本作业日志，获取主机磁盘容量数据并入库
    """
    start_time = datetime.datetime.now()
    while datetime.datetime.now() - start_time < datetime.timedelta(seconds=5):  # 5s作业还没执行完超时处理
        res = client.job.get_job_instance_log(**log_kwargs)
        if res.get('result'):
            data = res.get('data')[0]
            if data.get('is_finished'):
                log_content = data.get('step_results')[0].get(
                    'ip_logs')[0].get('log_content')
                host_informations = log_content.split('\n')[1:-1]
                for _information in host_informations:
                    _info_list = _information.split()
                    HostCapacity.objects.create(
                        filesystem=_info_list[0],
                        size=_info_list[1],
                        used=_info_list[2],
                        avail=_info_list[3],
                        used_percent=_info_list[4],
                        mounted=_info_list[5],
                        ip=ip,
                    )
                return True, '数据保存成功'
            else:
                sleep(1)  # 若作业还没执行结束，等待1s
        else:
            return False, '执行获取作业实例日志失败'
    return False, '作业实例执行超时'


# @periodic_task(run_every=crontab(minute='00', hour='*', day_of_week="*"))
@periodic_task(run_every=datetime.timedelta(seconds=7))
def save_disk_capacity():
    """
    周期性任务，调用快速作业脚本api，获取磁盘分区数据并入库
    """
    user = User.objects.get(username=844716598)
    client = get_client_by_user(user.username)  # 这里是周期任务，不能通过request请求client
    biz_id = 4  #测试业务
    ip = '10.0.1.80'
    script_kwargs = {
        'bk_biz_id': biz_id,
        'ip_list': [
            {
                'bk_cloud_id': 0,
                'ip': ip,
            }
        ],
        'account': 'root',
        'script_content': base64.b64encode(b'df -hl').decode('utf-8'),
    }

    # 调用快速脚本作业api，返回调用结果和作业实例id
    logger.info('调用快速脚本作业api')
    result, job_instance_id = get_fast_execute_script_job_instance_id(client, script_kwargs)

    if not result:
        logger.error('无法获取脚本实例')
        return
    else:
        logger.error('获取脚本实例')

    log_kwargs = {
        'bk_biz_id': biz_id,
        'job_instance_id': job_instance_id,
    }

    # 读取主机容量查询结果并入库
    result, msg = save_host_capacity_usage(client, ip, log_kwargs)

    if result:
        logger.info(msg)
    else:
        logger.error(msg)


@periodic_task(run_every=datetime.timedelta(seconds=1))
    logger.error('get disk work starting')
