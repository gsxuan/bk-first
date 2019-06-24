# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsGetCapacity(object):
    """Collections of get_disk_usage APIS"""

    def __init__(self, client):
        self.client = client

        self.get_disk_usage = ComponentAPI(
            client=self.client, method='GET',
            path='/api/c/self-service-api/api/get_disk_usage/',
            description=u'获取磁盘分区容量记录'
        )
