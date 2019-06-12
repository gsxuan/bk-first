# -*- coding: utf-8 -*-
from django.db import models, migrations
from django.forms.models import model_to_dict

# Create your models here.
#作业三
class HostModelManager(models.Manager):
    def to_dict(self):
        host_list = super().get_queryset()
        res_dict = [{
            'host_id': item.id,
            'host_name': item.host,
            'host_ip': item.ip,
            'host_df': item.df,
            'host_os': item.os,
            'host_note': item.note,
            'host_createtime': item.create_time.strftime("%y-%m-%d %H:%M:%S")
        } for item in host_list]
        return res_dict

class Hostlist(models.Model):
    SYSTEM_CHOICES = (
        ('Windows', 'Windows'),
        ('Linux', 'Linux'),
        ('Mac', 'Mac'),
    )
    host = models.CharField(max_length=30, verbose_name='主机名')
    ip = models.GenericIPAddressField(verbose_name='ip')
    df = models.CharField(max_length=100, verbose_name='磁盘分区')
    os = models.CharField(choices=SYSTEM_CHOICES ,max_length=30, verbose_name='系统平台')
    note = models.GenericIPAddressField(verbose_name='备注')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    
    objects = HostModelManager()


class DiskUsage(models.Model):
    value = models.IntegerField('磁盘使用率')
    add_time = models.DateTimeField('录入时间', auto_now=True)
    #host = models.ForeignKey(host, on_delete=models.CASCADE, related_name="DiskUsage")


#作业四
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
