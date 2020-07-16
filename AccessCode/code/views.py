from django.shortcuts import render
import json
from AccessCode import *
# Create your views here.
from django.http import HttpResponse


def index(request):
    """首页"""
    phone = ['+86 18141920039', 100, '1分钟']
    phone1 = ['+86 16210788973', 200, '2分钟']
    return render(request, 'index.html', context={'phone': phone})


def sim_content(request):
    return render(request, 'sim_content.html')


def sim_update(request):
    """最新短信写入数据库"""
    if request.method == 'POST':
        if request.POST:  # 判断是否传参
            Content = request.POST.get('Content', 0)
            time = request.POST.get('time', 0)
            Simnum = request.POST.get('Simnum', 0)
            Md5 = request.POST.get('Md5', 0)
            content = Content + ',' + time + ',' + Simnum + ',' + Md5
            article = json.dumps({
                'status': 200,
                'errorcode': 10001,
                'context': content},
                ensure_ascii=False)
            return HttpResponse(article, content_type='application/json')
        article = json.dumps({
            'status': 200,
            'errorcode': 10001,
            'context': 'cuole'},
            ensure_ascii=False)
        return HttpResponse(article, content_type='application/json')
        # try:
        #     content = uid + ',' + name + ',' + Countdown + ',' + url
        #     # 数据写入记录文件
        #     filename = 'API/config/access.txt'
        #     with open(filename, 'a+', encoding='UTF-8') as f:
        #         f.write(content)
        #         f.write('\n')
        #     article = json.dumps({
        #         'status': 200,
        #         'errorcode': 10001,
        #         'context': '数据写入成功!'},
        #         ensure_ascii=False)
        #     return HttpResponse(article, content_type='application/json')
        # except:
        #     article = json.dumps({
        #         'status': 200,
        #         'errorcode': 10002,
        #         'context': '数据写入失败!'},
        #         ensure_ascii=False)
        #     return HttpResponse(article, content_type='application/json')