from django.shortcuts import render
from django.http import HttpResponse
from blueking.component.shortcuts import get_client_by_request
# Create your views here.


def home(request):
    """
    首页
    """
    return render(request, 'get_capacity/home.html')


def render_json(dictionary={}):
    """
    return the json string for response
    @summary: dictionary也可以是string, list数据
    @note:  返回结果是个dict, 请注意默认数据格式:
                                    {'result': '',
                                     'message':''
                                    }
    """
    if type(dictionary) is not dict:
        # 如果参数不是dict,则组合成dict
        dictionary = {
            'result': True,
            'message': dictionary,
        }
    return HttpResponse(json.dumps(dictionary), content_type='application/json')

def get_app(request):
    """
    获取所有业务
    """
    app_list = []
    client = get_client_by_request(request)
    kwargs = {}
    resp = client.cc.get_app_list(**kwargs)

    if resp.get('result'):
        data = resp.get('data', [])
        for _d in data:
                app_list.append({
                    'name': _d.get('ApplicationName'),
                    'id': _d.get('ApplicationID'),
                })
        result = {'result' : resp.get('result'), 'data': app_list}
        return render_json(result)


# def get_ip_by_appid(request):
#     """
#     获取所有业务
#     """


# def get_task_list(request):
#     """
#     获取任务列表
#     """


# def execcute_task(request):
#     """
#     执行任务
#     """


# def get_capacity(request):
#     """
#     获取磁盘容量
#     """


# def get_capacity_chartdata(request):
#     """
#     获取数据
#     """

