from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    """首页"""
    phone = ['+86 18141920039', 100, '1分钟']
    phone1 = ['+86 16210788973', 200, '2分钟']
    return render(request, 'index.html', context={'phone': phone})


def sim_content(request):
    return render(request, 'sim_content.html')


li = ['q', 'w', 'e', 'r']
tu = ('a', 's', 'd', 'f')
dic = {'x': 1, 'y': 2}
st = 'this is django course'


def index2(request):
    """
    模板传值
    :param request:
    :return:
    """
    return render(request, 'movie_index.html',
                  context={'li': li,
                           'tu': tu,
                           'dic': dic,
                           'str': st})