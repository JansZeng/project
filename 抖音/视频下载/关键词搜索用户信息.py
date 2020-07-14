# -*- coding: utf-8 -*-
# @Time    : 2019/7/23 14:44
# @Author  : project
# @File    : 关键词搜索用户信息.py
# @Software: PyCharm
import csv
import requests
import json
from urllib.parse import quote
import time

ts = str(time.time()).split(".")[0]
_rticket = str(time.time() * 1000).split(".")[0]
headers={
        "X-Gorgon": '0404a0d802048185c98e95e9f257fed99bb4fbb9cf0019714e85',
        "X-Khronos": ts,
        "sdk-version":"1",
        "Accept-Encoding": "gzip",
        "X-SS-REQ-TICKET": _rticket,
        "Host": "search-hl.amemv.com",
        "Connection": "Keep-Alive",
        'User-Agent': 'okhttp/3.10.0.1',
        "x-tt-token": '0066d7f0c5f866ecfa0e3e0f6e55d8a49464f44daeaadcaaa7eaee497bcfb624f6f49690618c4329c7423eef0727d5256a17'
      }

count = 0


def post_html(url):
    """
    post方式获取html
    :param url:
    :return:
    """
    print(url)
    data = {'cursor':10,
            'keyword': '%E7%BE%8E%E9%A3%9F',
            'count': 10,
           'type': 1,
           'is_pull_refresh': 1,
           'hot_search': 0,
           'search_source': 'switch_tab',
            'search_id': '202007131617510101440630873402F1B0',
           'query_correct_type': 1,
            'enter_from': 'homepage_hot'}
    rsp = requests.post(url, headers=headers, data=data, verify=False)
    print(111)
    print(rsp.text)
    print(2)
    # return rsp.content.decode(rsp.apparent_encoding, 'ignore')
    return rsp.content.decode(encoding='utf-8')


def get_video(key):
    """
    根据关键词搜索用户信息
    :param key:
    :return:
    """
    # 编译关键词
    keys = quote(key)
    # 下一页
    cursor = 0
    while True:
        # 拼接用户搜索接口url
        # hot_search 0普通搜索 1热门搜索 type=1 用户列表
        # url = 'https://aweme-hl.snssdk.com/aweme/v1/discover/search/?cursor=' + str(cursor) + '&keyword=' + keys + '&offset=0&count=10&type=1&is_pull_refresh=0&hot_search=0&latitude=30.725991&longitude=103.968091&ts=1543984658&js_sdk_version=1.2.2&app_type=normal&manifest_version_code=350&_rticket=1543984657736&ac=wifi&device_id=60155513971&iid=53112482656&os_version=8.0.0&channel=xiaomi&version_code=350&device_type=MI%205&language=zh&uuid=862258031596696&resolution=1080*1920&openudid=8aa8e21fca47053b&update_version_code=3502&app_name=aweme&version_name=3.5.0&os_api=26&device_brand=Xiaomi&ssmix=a&device_platform=android&dpi=480&aid=1128&as=a1e5055072614ce6a74033&cp=5813c65d2e7d0769e1[eIi&mas=01327dcd31044d72007555ed00c3de0b5dcccc0c2cec866ca6c62c'
        url = 'https://search-hl.amemv.com/aweme/v1/discover/search/?ts=1594628278&cpu_support64=true&storage_type=2&host_abi=armeabi-v7a&_rticket=1594628278999&mac_address=32%3A8a%3Aee%3Ae5%3Aec%3Ae4&mcc_mnc=46011&'
        # 获取搜索界面并转化为json对象
        jsonObj = json.loads(post_html(url))
        print(jsonObj)
        metes = jsonObj['user_list']
        nums = len(metes)
        for _ in range(nums):
            # 抖音号
            short_id = metes[_]['user_info']['short_id']
            # UID
            uid = metes[_]['user_info']['uid']
            # 昵称
            nickname = metes[_]['user_info']['nickname']
            # 个性签名
            signature = metes[_]['user_info']['signature']
            signature = signature.replace('\n', '  ')
            # 性别 1=男 2=女 0=未知
            gender = metes[_]['user_info']['gender']
            gender = '男' if gender == 1 else '女' if gender == 2 else '未知'
            # 年龄
            birthday = metes[_]['user_info']['birthday']
            if birthday:
                birthday = birthday.split('-')[0]
                now_year = time.strftime("%Y", time.localtime())
                birthday = int(now_year) - int(birthday)
            # 粉丝
            follower = metes[_]['user_info']['follower_count']
            # 关注
            following = metes[_]['user_info']['following_count']
            # 赞
            total_favorited = metes[_]['user_info']['total_favorited']
            # 个人主页
            user_url = 'https://www.douyin.com/share/user/{}'.format(uid)
            # 读取时间
            writertime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            data = ([[key, short_id, nickname, signature, gender, birthday, follower, following, total_favorited, user_url, writertime]])
            model_csv(data)
        # 没有下一页数据退出
        if not jsonObj['has_more']:
            break
        cursor += 10
        time.sleep(3)


def model_csv(data):
    """保存数据"""

    global count
    count += 1
    with open("demo.csv", "a+", encoding='utf-8', newline="") as f:
        k = csv.writer(f, delimiter=',')
        with open("demo.csv", "r", encoding='utf-8', newline="") as f1:
            reader = csv.reader(f1)
            if not [row for row in reader]:
                k.writerow(['关键词', '抖音号', '昵称', '个性签名', '性别', '年龄', '粉丝', '关注', '赞', '个人主页', '写入时间'])
                k.writerows(data)
                print('第[{}]条数据插入成功'.format(count))
            else:
                k.writerows(data)
                print('第[{}]条数据插入成功'.format(count))


if __name__ == '__main__':
    key = input('请输入关键词：')
    get_video(key)