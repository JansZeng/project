#!/usr/bin/env python 
# encoding: utf-8
# @version: v1.0
# @author: xxxx
# @site: 
# @software: PyCharm
# @file: spider.py
# @time: 2019/9/3 13:01

"""
1.根据GUI写入数据拼接URL
  # 获取GUI写入数据保存至txt 主程序读取txt文件 拼接url
2.URL转换为短链接
  # 百度短链转换，每天一万条免费额度 至关重要 有些短链网站转换后会出现中文乱码
  # 中文需转码 quote
3.短链接生成二维码
  # 聚合数据 短链接生成二维码
  # 中文需转码 quote

短链接 转换 ：百度短链接
支付宝 转账接口：需要urlencode  from urllib.parse import quote
https://www.alipay.com/?appId=09999988&actionType=toCard&sourceId=bill&cardNo=银行卡号&bankAccount=银行账户名&money=转账金额&amount=备注&bankMark=银行英文简写&bankName=银行中文名称
查询银行代码
https://ccdcapi.alipay.com/validateAndCacheCardInfo.json?cardNo=填写卡号&cardBinCheck=true

alipays://platformapi/startapp?appId=09999988&actionType=toCard&sourceId=bill&cardNo=6217000030001234567&bankAccount=%E9%A9%AC%E4%BA%91&money=0.01&amount=0.01&bankMark=CCB&bankName=%E4%B8%AD%E5%9B%BD%E5%BB%BA%E8%AE%BE%E9%93%B6%E8%A1%8C
参数：
appId=09999988   // 应用ID -默认
actionType=toCard  // 转账类型 toCard-到银行卡
sourceId=bill  // 未知
cardNo=6217000030001234567  // 银行卡号
bankAccount=%E9%A9%AC%E4%BA%91  // 银行账户
money=0.01  // 转账金额
amount=0.01  // 转账额度
bankMark=CCB  // 银行代号 -可选
bankName=%E4%B8%AD%E5%9B%BD%E5%BB%BA%E8%AE%BE%E9%93%B6%E8%A1%8C  // 银行名称

接口：
    转账到银行卡：
        https://www.alipay.com/?appId=09999988&actionType=toCard&sourceId=bill&cardNo=622203***4880&bankAccount=陈建军&money=1&amount=1&bankMark=ICBC&amp;bankName=工商银行&cardIndex=1909221389508861750&cardNoHidden=true&cardChannel=HISTORY_CARD&orderSource=from&buyId=auto
    转账到支付宝账户：
        https://ds.alipay.com/?from=mobilecodec&scheme=alipays%3A%2F%2Fplatformapi%2Fstartapp%3FappId%3D20000200%26actionType%3DtoAccount%26account%3D{支付宝账号}%26amount%3D%26memo%3D
    跳转到转账页面：
        # auth_base 无需用户授权获取userID
        userId：获取方法 https://www.dedemao.com/alipay/authorize_demo.php?scope=auth_base
        https://www.alipay.com/?appId=09999988&actionType=toAccount&goBack=NO&amount=1.00&userId=2088902532716171&memo=QQ_1033383881
"""
import os
import json
import string
import requests
from urllib.parse import quote  # url编码
from fake_useragent import UserAgent

from image_process import Picture


class Spider:
    def __init__(self):
        self.headers = {'user-agent': str(UserAgent().random)}

    def get_url(self, lang_url):
        """
        长链接转换端链接 百度短链
        0：正常返回短网址
        -1：短网址生成失败
        -2：长网址不合法
        -3：长网址存在安全隐患
        -4：内部错误
        -5：短网址服务目前不支持该域名
        -6：有效期设置错误
        -7：长网址在安全检测中
        -1xx：Token验证失败
        :param lang_url:
        :return:
        """
        # url 中文转码  string.printable 跳过ascii码
        lang_url = quote(lang_url, string.printable)

        host = 'https://dwz.cn'
        path = '/admin/v2/create'
        url = host + path
        method = 'POST'
        content_type = 'application/json'
        # 设置Token
        token = '5e5dae6521ca463a43aa1063335e3792'
        # 设置待创建的长网址
        bodys = {'Url': lang_url, 'TermOfValidity': '1-year'}
        # 配置headers
        headers = {'Content-Type': content_type, 'Token': token}
        count = 1
        while True:
            # 发起请求
            response = requests.post(url=url, data=json.dumps(bodys), headers=headers)
            # 读取响应
            response = json.loads(response.text)
            if count > 3:
                print('程序运行错误,请联系开发者!')
                os._exit(0)
            if response['Code']:
                print('错误代码：{} 重试'.format(response['Code']))
                count += 1
                continue

            return response['ShortUrl']

    def code_generate(self, short_link):
        """
        聚合数据 短链接生成二维码
        https://www.juhe.cn/box/index/id/296 错误码参照表
        二维码生成
        :return:
        """
        # 转码
        short_link = quote(short_link, string.digits)
        url = 'http://apis.juhe.cn/qrcode/api?text={}&el=&bgcolor=&fgcolor=&logo=&w=&m=&lw=&type=2&key=b142a4a659dfa5237bf54a78baf8382f'.format(short_link)
        response = requests.get(url, headers=self.headers)
        with open('image/code.png', 'wb') as f:
            f.write(response.content)
            print('支付宝转账码生成成功!')
    
    def read_txt(self):
        """
        读取界面输入数据文件
        :return: 
        """
        # 获取当前目录
        path = os.getcwd()
        # 返回指定目录下所有文件
        files = os.listdir(path)
        # 筛选指定文件
        files = [i for i in files if 'config.txt' in i]
        if not files:
            print('读取配置文件错误,请正确填写数据!')
            os._exit(0)

        with open(files[0], 'r', encoding='UTF-8') as f:
            content = f.read().split(',')
            content = [i for i in content if i]
            content = content + ['ABC', '中国农业银行'] if len(content) < 5 else content
            return content

    def run(self):
        content = self.read_txt()
        # 跳转到转账页面
        # _url = f'https://www.alipay.com/?appId=09999988&actionType=toAccount&goBack=NO&amount=&userId={2088632465859457}&memo='

        # 跳转到支付宝账户页面
        alipay = '16506570622'
        _url = f'https://ds.alipay.com/?from=mobilecodec&scheme=alipays%3A%2F%2Fplatformapi%2Fstartapp%3FappId%3D20000200%26actionType%3DtoAccount%26account%3D{alipay}%26amount%3D%26memo%3D'

        # 长链接生成短链
        short_link = self.get_url(_url)
        # 短链生成二维码
        self.code_generate(short_link)
        # 图片处理
        image_process = Picture()
        image_process.text = content[2]
        image_process.run()


if __name__ == '__main__':
    spider = Spider()
    spider.run()
