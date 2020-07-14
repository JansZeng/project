# -*- coding:utf-8 -*-
# 文件 ：mitmdump_server.py
# IED ：PyCharm
# 时间 ：2019/10/30 0030 16:37
# 版本 ：V1.0
"""
切换至脚本目录下运行脚本
mitmdump -s mitmdump_server.py
OSError: [WinError 87] 参数错误 : 把print注释掉
"""
import csv
import json
import datetime


def response(flow):
    url = 'https://search-hl.amemv.com/aweme/v1/discover/search'
    # print(url)`
    # 筛选出以上面url为开头的url
    if flow.request.url.startswith(url):
        # 获取评论json数据
        text = flow.response.text
        # 将已编码的json字符串解码为python对象
        content = json.loads(text)
        print(content)
        user_list = content['user_list']
        for user in user_list:
            short_id = user['user_info']['short_id']
            nickname = user['user_info']['nickname']
            signature = user['user_info']['signature']
            signature = str(signature).replace('\n', '')
            save_data([[short_id, nickname, signature]])


def save_data(data):
    """保存为csv"""
    filename = datetime.datetime.now().strftime('%Y-%m-%d') + '.csv'
    with open(filename, "a+", encoding='gbk', newline="") as f:
        k = csv.writer(f, delimiter=',')
        with open(filename, "r", encoding='gbk', newline="") as f1:
            reader = csv.reader(f1)
            if not [row for row in reader]:
                k.writerow(['ID', '昵称', '简介'])
                k.writerows(data)
            else:
                k.writerows(data)
