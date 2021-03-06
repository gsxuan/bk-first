# coding: utf-8

import datetime
from time import sleep

from .models import HostCapacity


def get_fast_execute_script_job_instance_id(client, script_kwargs):
    """
    调用快速执行脚本api并返回作业状态和实例id
    """
    res = client.job.fast_execute_script(**script_kwargs)
    job_instance_id = res.get('data').get('job_instance_id') if res.get('result') is True else -1
    return res.get('result'), job_instance_id


def save_get_capacity_usage(client, ip,  log_kwargs):
    """
    读取快速执行脚本作业日志，获取主机磁盘容量数据并入库
    """
    start_time = datetime.datetime.now()
    while datetime.datetime.now() - start_time < datetime.timedelta(seconds=5):  # 5s作业还没执行完超时处理
        res = client.job.get_job_instance_log(**log_kwargs)
        if res.get('result'):
            data = res.get('data')[0]
            if data.get('is_finished'):
                log_content = data.get('step_results')[0].get('ip_logs')[0].get('log_content')
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

