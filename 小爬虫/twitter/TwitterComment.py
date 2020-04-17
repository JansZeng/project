# -*- coding:utf-8 -*-
# 文件 ：TwitterComment.py
# IED ：PyCharm
# 时间 ：2020/4/16 0016 16:19
# 版本 ：V1.0
import os
import socket
import sys
import csv
import time
import logging
import datetime
from configparser import ConfigParser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

print(os.path.abspath(__file__))  # 当前文件绝对路径
PATH = os.getcwd()  # 文件路径


def run_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.datetime.now()
        log_init().info("Program start time：{}".format(start_time))
        res = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        log_init().info("Program end time：{}".format(end_time))
        log_init().info("Program execution time：{}s".format((end_time - start_time)))
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
        path = PATH + r'/logs/'  # 日志保存路径
        if not os.path.exists(path):
            os.mkdir(path)
        filename = path + datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        fh = logging.FileHandler(filename, encoding='utf-8', mode='a+')  # 设置日志信息保存至文件
        # fh.setLevel(logging.DEBUG)  # 设置日志器输出级别
        fh.setFormatter(formatter)  # 设置日志输出格式
        logger.addHandler(fh)
        logger.addHandler(console)

    return logger


class Twitter:
    def __init__(self):
        log_init().info('Program start')
        log_init().info('init chrome')

        # 开启mitmdump
        self.monitor = Monitor()
        self.monitor.run()

        options = Options()
        # 使用无头模式
        options.add_argument('headless')
        options.add_argument('--disable-gpu')
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        prefs = {"profile.managed_default_content_settings.images": 2}  # 1 加载图片 2不加载图片,加快访问速度
        options.add_experimental_option("prefs", prefs)
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(chrome_options=options, desired_capabilities=desired_capabilities)

        self.wait = WebDriverWait(self.driver, 10, 1)  # 设置隐式等待时间
        self.driver.maximize_window()  # 窗口最大化
        log_init().info('chrome initialized successfully')

    def set_ini(self, section, name, val):
        """读取、修改 ini配置文件"""
        file = PATH + '\config\config.ini'  # 文件路径
        cp = ConfigParser()  # 实例化
        cp.read(file, encoding='utf-8')  # 读取文件
        cp.set(section, name, val)  # 修改数据
        with open(file, 'w', encoding='utf-8') as f:
            cp.write(f)
        log_init().info(f'成功写入配置文件：{val}')

    def red_csv(self):
        """读取ID配置文件"""
        with open('config/ID数据.csv', 'r', encoding='UTF-8-sig') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                yield row[0]

    def keep_records(self, model_id, vali=False):
        """保存获取记录"""
        file_name = f'{PATH}/config/valida.txt'
        if not os.path.exists(file_name):
            fi = open(file_name, 'a')
            fi.close()
        if vali:
            with open(file_name, 'r') as f:
                flight = [i.replace('\n', '') for i in f.readlines()]
                if model_id in flight:
                    return True
                return False
        else:
            with open(file_name, 'a+') as f:
                f.write(model_id)
                f.write('\n')

    def get_basic(self, url):
        while True:
            count = 0
            self.driver.get(url)
            if url not in self.driver.current_url:
                continue
            while True:
                log_init().info('Data acquisition...')
                if count > 10:
                    return
                Height = self.driver.execute_script("return document.body.scrollHeight;")
                # 获取body的高度，滑到底部
                scroll = "window.scrollTo(0,document.body.scrollHeight)"
                self.driver.execute_script(scroll)
                time.sleep(2)
                # 判断是否到达底部
                page_source = self.driver.page_source
                if'显示更多回复' in page_source or 'Show more replies' in page_source:
                    # print('没有更多数据')
                    return
                new_Height = self.driver.execute_script("return document.body.scrollHeight;")
                if new_Height == Height:
                    count += 1
                else:
                    count = 0
                # print(count)

    @run_time
    def main(self):
        log_init().info('Read ID data files...')
        for url in self.red_csv():
            # 判断是否获取过
            if self.keep_records(url, vali=True):
                print(f'{url} jump over!')
                continue
            log_init().info(f'{url}Data acquisition...')
            # 写入配置文件
            ID = url.split('/')[-1]
            print(ID)
            self.set_ini('Version', 'id', ID)
            # 翻页获取数据
            try:
                self.get_basic(url)
            except Exception as e:
                log_init().error(e)
                continue
            log_init().info(f'{url}Data acquisition completed!')

            # 写入获取记录
            self.keep_records(url)
            log_init().info('Save acquisition records')

        self.driver.quit()
        # 关闭mitmduimp
        self.monitor.kill()


class Monitor:
    def net_is_used(self, port, ip='127.0.0.1'):
        """
        检测端口是否被占用
        :param port: 端口
        :param ip:IP地址
        :return:
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            s.shutdown(2)
            # print(f'sorry, {ip}:{port} 端口已被占用!')
            return True
        except Exception as e:
            # print(f'{ip}:{port}端口未启用!')
            log_init().error(e)
            return False

    def switch_mitmdump(self):
        """启动mitmdump服务"""
        log_init().info('Kill mitmdump Server')
        mitmdump = 'taskkill /F /IM mitmdump.exe'
        cmd = 'taskkill /F /IM cmd.exe'
        os.system(mitmdump)
        os.system(cmd)
        log_init().info('Start mitmdump Server')
        os.system('start /min mitmdump --mode upstream:https://127.0.0.1:1080 -s mitmdump_server.py')
        time.sleep(5)
        if not self.net_is_used(8080):
            log_init().info('mitmdump Service failed to start!')
            os._exit(0)
        log_init().info('mitmdump Service started successfully!')

    def kill(self):
        mitmdump = 'taskkill /F /IM mitmdump.exe'
        cmd = 'taskkill /F /IM cmd.exe'
        os.system(mitmdump)  # 杀死mitmdump进程
        os.system(cmd)  # 关闭命令行窗口
        log_init().info('Kill mitmdump Server')

    def run(self):
        self.switch_mitmdump()


if __name__ == '__main__':
    twitter = Twitter()
    twitter.main()