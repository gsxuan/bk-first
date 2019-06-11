# coding:utf-8

from django.db import models
from django.forms.models import model_to_dict


class HostCapacityManager(models.Manager):
    def get_disk_list(self):
        """
        获取分区列表
        """
        return [qs['mounted'] for qs in super().get_queryset().values('mounted').distinct().order_by('mounted')]

    def get_disk_data(self, disk):
        """
        获取分区数据
        """
        return super().get_queryset().filter(mounted=disk)

    def get_ip_list(self):
        """
        获取ip列表
        """
        return [qs['ip'] for qs in super().get_queryset().values('ip').distinct().order_by('ip')]

    def get_disk_list_based_on_ip(self, ip):
        """
        基于ip获取分区列表
        """
        return [qs['mounted'] for qs in
                super().get_queryset().filter(ip=ip).values('mounted').distinct().order_by('mounted')]

    def get_disk_data_based_on_ip(self, ip, disk):
        """
        基于ip和分区获取磁盘容量
        """
        qs = super().get_queryset().filter(ip=ip, mounted=disk).order_by('-create_time')
        return None if len(qs) == 0 else model_to_dict(qs[0])


class HostCapacity(models.Model):
    ip = models.CharField('ip', max_length=64)
    filesystem = models.CharField('filesystem', max_length=64)
    size = models.CharField('size', max_length=64)
    used = models.CharField('used', max_length=64)
    used_percent = models.CharField('used_percent', max_length=64)
    avail = models.CharField('avail', max_length=64)
    mounted = models.CharField('mounted', max_length=64)
    create_time = models.DateTimeField('create time', auto_now=True)

    objects = HostCapacityManager()

    def __str__(self):
        return self.mounted

    class Meta:
        verbose_name = verbose_name_plural = '磁盘容量数据'


class HostCapacityApiCheckRecord(models.Model):
    ip = models.CharField('ip', max_length=64)
    mounted = models.CharField('mounted', max_length=64)
    used_percent = models.CharField('used_percent', max_length=64)
    check_time = models.DateTimeField('check time', auto_now=True)

    def __str__(self):
        return '{} {} {} {}'.format(self.ip, self.mounted, self.used_percent, self.check_time)

    class Meta:
        verbose_name = verbose_name_plural = 'API磁盘容量查询记录'
