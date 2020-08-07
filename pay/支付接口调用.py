# coding=utf-8
# 作者    ： Administrator
# 文件    ：123.py
# IED    ：PyCharm
# 创建时间 ：2020/5/24 11:09
import base64
import random
import datetime
import hashlib
import requests


def getQRcode():
    """请求支付二维码"""
    # 接口地址
    url = 'http://pay.ccccc.run/index/api/getQRcode'
    # 订单号 由当前时间的年月日时分秒和五位随机数字组成。一个订单号只能调用一次接口，每次调用接口应该更新订单号
    order_id = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(10000, 99999)}"
    # 金额
    money = 0.01
    # 回调地址
    return_url = 'http://www.dongdongmeiche.cn/ceshi'
    # 支付方式 wechat  或  ali
    method = 'wechat'
    # md5加密串 密钥key,order_id订单号,money金额,return_url回调地址,method支付方法依次拼接md5加密  密钥key固定为sdl2fL3KH3J3G92327Kh
    key = f'sdl2fL3KH3J3G92327Kh{order_id}{money}{return_url}{method}'
    md5str = hashlib.md5(key.encode()).hexdigest()

    print('请求地址：')
    print(f'{url}?order_id={order_id}&money={money}&return_url={return_url}&method={method}&md5str={md5str}')
    # 请求数据
    res = requests.get(f'{url}?order_id={order_id}&money={money}&return_url={return_url}&method={method}&md5str={md5str}').json()
    if res['flag'] != '10000':
        print(res['msg'])
        return
    qr_img = res['info']['qr_img']
    base64_data = qr_img.split(',')[-1]
    print('数据请求成功!')
    with open('支付二维码.jpg', 'wb') as file:
        img = base64.b64decode(base64_data)
        file.write(img)
    print('支付二维码保存成功!')


def test():
    # 订单号 由当前时间的年月日时分秒和五位随机数字组成。一个订单号只能调用一次接口，每次调用接口应该更新订单号
    order_id = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(10000, 99999)}"
    # md5加密串 密钥key,order_id订单号,money金额,return_url回调地址,method支付方法依次拼接md5加密  密钥key固定为sdl2fL3KH3J3G92327Kh
    key = f'sdl2fL3KH3J3G92327Kh{order_id}'
    print(key)
    md5str = hashlib.md5(key.encode()).hexdigest()
    print(md5str)
    url = f'http://pay.ccccc.run/index/api/getQRcode?order_id={order_id}&md5str={md5str}'
    print(url)
    resp = requests.get(url)
    print(resp.text)
    # print(resp.json())


if __name__ == '__main__':
    # getQRcode()
    test()