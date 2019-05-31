# -*- coding: utf-8 -*-
from django.db import models, migrations
# Create your models here.
class HostModelManager(models.Manager):
    def to_dict(self):
        host_list = super().get_queryset()
        res_dict = [{
            'host_id': item.id,
            'host_name': item.name,
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
    name = models.CharField(max_length=30, verbose_name='主机名')
    ip = models.GenericIPAddressField(verbose_name='ip')
    df = models.CharField(max_length=100, verbose_name='磁盘分区')
    os = models.CharField(choices=SYSTEM_CHOICES ,max_length=30, verbose_name='系统平台')
    note = models.GenericIPAddressField(verbose_name='备注')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    
    objects = HostModelManager()
