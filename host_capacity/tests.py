# coding: utf-8

import json

from django.test import TestCase, Client
from django.shortcuts import reverse

from config import API_TOKEN
from host_capacity import host_capacity_apis
from host_capacity.models import HostCapacity
# Create your tests here.


class ApiTestCase(TestCase):
    """
    测试磁盘容量查询API调用逻辑
    """

    def setUp(self):
        self.client = Client()
        HostCapacity.objects.create(ip='1.1.1.1', mounted='/', size='50G', used='10G',
                                    used_percent='20%', avail='40G')

    def _visit_api(self, api_params):
        json_response = self.client.get(reverse(host_capacity_apis.get_host_capacity_api), api_params)
        response = json.loads(json_response.content)
        return response

    def test_api_token(self):
        response = self._visit_api({})
        self.assertEqual(response['result'], False)
        self.assertEqual(response['message'], 'token illegal.')

    def test_api_ip_list(self):
        response = self._visit_api({'token': API_TOKEN})
        self.assertEqual(response['message'], 'ip list')

    def test_api_disk_list(self):
        response = self._visit_api({'token': API_TOKEN, 'ip': '1.1.1.1'})
        self.assertEqual(response['message'], 'disk list')

    def test_api_capacity_data_when_data_in_db(self):
        response = self._visit_api({'token': API_TOKEN, 'ip': '1.1.1.1', 'mounted': '/'})
        self.assertIsInstance(response['data'], dict)

    def test_api_when_no_data_in_db(self):
        HostCapacity.objects.all().delete()
        self.test_api_token()
        self.test_api_ip_list()
        self.test_api_disk_list()
        response = self._visit_api({'token': API_TOKEN, 'ip': '1.1.1.1', 'mounted': '/'})
        self.assertEqual(response['message'], 'get disk data failed.')
