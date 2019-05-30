# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class HostModelManager(models.Manager):
    def to_dict(self):
        qs = super().get_queryset()
        res_dict = [{
            'host_name': item.name,
            'host_ip': item.ip,
            'host_os': item.os,
            'host_note': item.note,
            'host_creattime': item.record_time.strftime("%y-%m-%d %H:%M:%S")
        } for item in qs]
        return res_dict


class HostModel(models.Model):
    SYSTEM_CHOICES = (
        ('Windows', 'Windows'),
        ('Linux', 'Linux'),
        ('Mac', 'Mac'),
    )
    name = models.CharField(max_length=30, verbose_name='主机名')
    ip = models.GenericIPAddressField(verbose_name='ip')
    os = models.CharField(choices=SYSTEM_CHOICES ,max_length=30, verbose_name='系统平台')

    objects = HostModelManager()
