from django.shortcuts import render
import json
import datetime
import requests
from django.http import HttpResponse
from retrying import retry
from .models import SmsContent  # 导入数据库模型类


def index(request):
    """首页"""
    phone = ['+86 18141920039', 112, '1分钟']
    phone1 = ['+852 55926036', 135, '2分钟']
    phone2 = ['+852 55919590', 375, '2分钟']
    phone3 = ['+09 88827 5899', 421, '2分钟']
    phone4 = ['+09 25998 2911', 154, '2分钟']
    phone5 = ['+09 25368 3119', 78, '2分钟']
    get_sim_data()
    return render(request, 'index.html', context={'phone': phone,
                                                  'phone1': phone1,
                                                  'phone2': phone2,
                                                  'phone3': phone3,
                                                  'phone4': phone4,
                                                  'phone5': phone5})


def sim_content(request):
    contents = get_sim_data()
    # 数据库没有数据
    if not contents:
        return render(request, 'sim_content.html')
    # 判断是否够一页数据 6条
    contexts = {}
    for i in range(len(contents)):
        contexts[f'content{i}'] = contents[i]
    if len(contents) < 6:
        for i in range(len(contents), 6):
            contexts[f'content{i}'] = contents[len(contents) - 1]
    print(contexts)
    return render(request, 'sim_content.html', context=contexts)


def ip(request):
    """获取访问客户端ip地址"""
    ip = None
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        if request.META.get("REMOTE_ADDR"):
            ip = request.META.get("REMOTE_ADDR")
        else:
            ip = request.META.get("HTTP_X_FORWARDED_FOR")

    # 获取物理地址
    try:
        address = ip_address(ip)
    except:
        address = '获取失败'
    return HttpResponse(f'{ip} {address}')


@retry(stop_max_attempt_number=5)
def ip_address(ip):
    """ip地址查询物理地址"""
    url = f'http://api.map.baidu.com/location/ip?ak=VCyE5wE5Wmo19kgLodBkbt0n5obyji5j&ip={ip}&coor=bd09ll'
    rsp = requests.get(url, timeout=10).text
    content = json.loads(rsp)

    # 请求状态 0有数据 1无数据
    status = content['status']
    if status:
        return content['message']
    address = content['content']['address']
    return address


def get_sim_data():
    """读取数据库数据"""
    # 根据id和电话号码倒序查询6条数据
    contents = SmsContent.objects.order_by('-id').filter(simnum='18210836362')[:6]
    print(contents)
    return contents


def sim_update(request):
    """最新短信写入数据库"""
    if request.method == 'POST':
        if request.POST:  # 判断是否传参
            Number = request.POST.get('number', 0)
            Content = request.POST.get('content', 0)
            time = request.POST.get('time', 0)
            Simnum = request.POST.get('simnum', 0)
            Md5 = request.POST.get('md5', 0)
            print(time)
            # 判断时间格式是否正确
            if validate(time):
                article = json.dumps({
                    'status': 200,
                    'errorcode': 10004,
                    'context': '时间格式错误：%Y-%m-%d %H:%M:%S'},
                    ensure_ascii=False)
                return HttpResponse(article, content_type='application/json')
            # SmsContent.objects.create(content=Content, time=time, simnum=Simnum, md5=Md5)
            # get_or_create插入前会判断有没有重复数据如果有不会添加
            a, b = SmsContent.objects.get_or_create(number=Number, content=Content, time=time, simnum=Simnum, md5=Md5)
            if b:
                content = '数据写入成功'
            else:
                content = '数据重复跳过'

            article = json.dumps({
                'status': 200,
                'errorcode': 10001,
                'context': content},
                ensure_ascii=False)
            return HttpResponse(article, content_type='application/json')

        # 参数错误
        article = json.dumps({
            'status': 200,
            'errorcode': 10002,
            'context': '参数错误'},
            ensure_ascii=False)
        return HttpResponse(article, content_type='application/json')


def validate(date_text):
    """判断时间格式"""
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return True
