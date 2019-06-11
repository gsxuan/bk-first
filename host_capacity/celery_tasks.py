# coding:utf-8

import base64

from celery.schedules import crontab
from celery.task import periodic_task

from blueking.component.shortcuts import get_client_by_user
from .api_utils import get_fast_execute_script_job_instance_id, save_host_capacity_usage
from blueapps.utils.logger import logger


@periodic_task(run_every=crontab(minute='00', hour='*', day_of_week="*"))
def save_disk_capacity():
    """
    周期性任务，调用快速作业脚本api，获取磁盘分区数据并入库
    """
    client = get_client_by_user('844716598')
    biz_id = 4
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
    result, job_instance_id = get_fast_execute_script_job_instance_id(client, script_kwargs)

    if not result:
        logger.error('无法获取脚本实例')
        return

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


