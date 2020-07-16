from django.test import TestCase

# Create your tests here.
import requests
import os

def upload(uid, name, Countdown, url):
    """向服务器上传数据"""
    _url = f'http://www.ccccc.run/sim_update/'
    data = {'Content': uid, 'time': name, 'Simnum': Countdown, 'Md5': url}
    print(data)
    response = requests.post(_url, data=data)
    print(response.text)
    content = response.json()
    code = content['errorcode']
    if code != 10001:
        print(content['context'])
        os._exit(0)
    print(content['context'])
    try:
        content = response.json()
        code = content['errorcode']
        if code != 10001:
            print(content['context'])
            os._exit(0)
        print(content['context'])
    except Exception as e:
        print('连接服务器错误!')
        print(e)


if __name__ == '__main__':
    upload('【智能航班】IP账号：ba618b3e3adc4e7c93127546d58502a5 即将到期及时续费!', '2020-07-15 17:37:34', '18210836362', '132')