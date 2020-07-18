# """
# 流量脚本
# 问题：phantomjs path 错误
# 解决：browser = webdriver.PhantomJS(executable_path=r'C:\Users\lyh\Anaconda2\phantomjs-2.1.1-windows\bin\phantomjs.exe')
# 下载地址：http://phantomjs.org/download.html解压把文件设置文件路径
# """

# coding=utf-8
# from selenium import webdriver
#
# # 代理服务器
# proxyHost = "218.91.7.6"
# proxyPort = "28803"
# proxyType = 'https'  # socks5
#
# # 代理隧道验证信息
# service_args = [
#     "--proxy-type=%s" % proxyType,
#     "--proxy=%(host)s:%(port)s" % {
#         "host": proxyHost,
#         "port": proxyPort,
#     }
# ]
# # 要访问的目标页面
# targetUrl = "http://www.ccccc.run"
# driver = webdriver.PhantomJS(executable_path=r'C:\Users\Administrator\Desktop\phantomjs-2.1.1-windows\bin\phantomjs.exe', service_args=service_args)
# driver.get('http://www.ccccc.run/ip')
# print(driver.page_source)
# time.sleep(3)
#
# driver.get(targetUrl)
#
# print(driver.title)
# driver.quit()

# if __name__ == '__main__':
#     while True:
#         test()
import os
import sys
import time
import random
import logging
import datetime
import requests
import threading
from selenium import webdriver

_PATH = os.getcwd()


def run_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.datetime.now()
        # print("程序开始时间：{}".format(start_time))
        log_init().info("程序开始时间：{}".format(start_time))
        res = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        # print("程序结束时间：{}".format(end_time))
        # print("程序执行用时：{}s".format((end_time - start_time)))
        log_init().info("程序结束时间：{}".format(end_time))
        log_init().info("程序执行用时：{}s".format((end_time - start_time)))
        return res

    return new_func


def log_init():
    # 创建一个日志器
    program = os.path.basename(sys.argv[0])  # 获取程序名
    logger = logging.getLogger(program)
    # 判断handler是否有值,(避免出现重复添加的问题)
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s | %(name)-3s | %(levelname)-6s| %(message)s')  # 设置日志输出格式
        logger.setLevel(logging.DEBUG)

        # 输出日志至屏幕
        console = logging.StreamHandler()  # 设置日志信息输出至屏幕
        console.setLevel(level=logging.DEBUG)  # 设置日志器输出级别，包括debug < info< warning< error< critical
        console.setFormatter(formatter)  # 设置日志输出格式

        # 输出日志至文件
        path = _PATH + r'/logs/'  # 日志保存路径
        if not os.path.exists(path):
            os.mkdir(path)
        filename = path + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        fh = logging.FileHandler(filename, encoding='utf-8', mode='a+')  # 设置日志信息保存至文件
        # fh.setLevel(logging.DEBUG)  # 设置日志器输出级别
        fh.setFormatter(formatter)  # 设置日志输出格式
        logger.addHandler(fh)
        logger.addHandler(console)

    return logger


class Proxy(object):
    def __init__(self):
        # 成功次数
        self.success_count = 0
        # 失败次数
        self.failure_count = 0

    def getdriver(self, ip):
        """初始化浏览器"""
        options = webdriver.ChromeOptions()
        # 使用无头模式
        options.add_argument('headless')
        # 添加代理
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 解决获取适配器失败
        options.add_argument(f"--proxy-server=http://{ip}")
        driver = webdriver.Chrome(chrome_options=options)
        # 限定页面加载超时时间最大为30秒
        driver.set_page_load_timeout(30)
        return driver

    def getpage(self, urls, ip, driver):
        # 检查代理ip
        # driver.get('http://www.ccccc.run/ip')
        # page_source = driver.page_source
        # if 'http://ccccc.run/ip' not in page_source:
        #     print('代理IP失效，切换下一个')
        #     return
        # print(driver.page_source)
        for url in urls:
            # 请求首页
            log_init().info(f'{ip} 请求 {url} 首页')
            driver.get(url)
            title = driver.title
            if '免费在线接码平台' not in title:
                log_init().info(f'{ip} 失效，切换下一个')
                return False
            # log_init().info(driver.title)

            # 请求详情页
            # 随机休眠
            sleep = random.randint(10, 30)
            sleep1 = random.randint(60, 90)
            log_init().info(f'{ip} 请求 {url} 详情页中 预计{sleep + 15 * 2 + sleep1}秒完成...')
            time.sleep(sleep)

            for i in range(random.randint(1, 3)):
                driver.get(f'{url}/sim')

                if '免费在线接码平台' not in driver.title:
                    return True
                time.sleep(random.randint(10, 20))
            # time.sleep(sleep1)
        return True

    def run(self, urls, ip):
        driver = self.getdriver(ip)
        try:
            if self.getpage(urls, ip, driver):
                # 成功次数计数
                self.success_count += 1
            else:
                # 失败次数计数
                self.failure_count += 1
        except:
            log_init().info(f'{ip} 请求出错，切换下一个。')
            driver.quit()
            # 失败次数计数
            self.failure_count += 1
            return
        # finally:
        log_init().info(f'{ip}请求完毕 关闭浏览器!')
        driver.quit()


def get_ip():
    """请求代理IP"""
    qty = 5
    url = f'http://120.79.85.144/index.php/api/entry?method=proxyServer.tiqu_api_url&packid=2&fa=0&fetch_key=&groupid=0&qty={qty}&time=1&port=1&format=json&ss=5&css=&ipport=1&et=1&pi=1&co=1&pro=&city=&dt=1&auth=0&ipnum=10&userip=1&auth_key=fnp63K6ncap_p3XYhHWpaX6ieamEspeZs4uUs7mYkGqXfYfUu7plZ5O6eteZeM-wfnx5rA&usertype=22'
    res = requests.get(url).json()
    if not res.get('data'):
        log_init().info('获取代理ip失败')
        log_init().info(res.get('msg'))
        os._exit(0)
    ips = [i.get('IP') for i in res.get('data') if i.get('IP')]
    log_init().info(ips)
    for ip in ips:
        yield ip


@run_time
def main():
    proxy = Proxy()
    count = 0
    urls = ['http://www.ccccc.run', 'http://www.dongdongmeiche.com']
    while True:
        if count >= 5:
            break
        # 创建线程对象
        thread_list = list()
        for ip in get_ip():
            count += 1
            thread_list.append(threading.Thread(target=proxy.run, args=(urls, ip)))

        # 启动所有线程
        for thread in thread_list:
            thread.start()
            time.sleep(random.randint(40, 60))

        # 主线程中等待所有子线程退出
        for thread in thread_list:
            thread.join()
    log_init().info(f'成功：{proxy.success_count}次')
    log_init().info(f'失败：{proxy.failure_count}次')


if __name__ == '__main__':
    main()
