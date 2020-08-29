import re
import os
import csv
import time
import shutil
import datetime
import requests
from lxml import etree
from PIL import Image
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Spider:
    def __init__(self):
        chrome_options = Options()
        # keep_alive 设置浏览器连接活跃状态
        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
        prefs = {"profile.managed_default_content_settings.images": 1}  # 1 加载图片 2不加载图片,加快访问速度
        chrome_options.add_experimental_option("prefs", prefs)
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 有界面模式
        self.driver = webdriver.Chrome(chrome_options=chrome_options, keep_alive=False)
        # 隐形等待时间
        self.wait = WebDriverWait(self.driver, 10, 0.5)
        # 浏览器窗口最大化
        self.driver.maximize_window()
        # 文件名
        self.file_name = None

    def get_code(self):
        """
        筛选所在地区数据获取url
        :return:
        """
        url = 'https://www.landchina.com/default.aspx?tabid=263&ComName=default&tdsourcetag=s_pcqq_aiomsg'
        self.driver.get(url)
        name = input('筛选数据：')
        # 获取页数
        page_num = self.driver.find_element_by_css_selector('.pager .pager:nth-child(1)')
        print(page_num.text)
        page_num = re.findall(r'共(.*?)页', page_num.text)[0]
        page_num = 200 if int(page_num) > 200 else page_num
        print(page_num)
        for num in range(2, int(page_num)+2):
            # print('第：{}页数据获取中'.format(num-1))
            # 定位到数据标签
            res = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="TAB_contentTable"]')))
            # 提取出数据标签
            html = res.get_attribute('innerHTML')

            # 获取详情url
            urls = re.findall(r'href="(.*?)"', html, re.S | re.M)
            urls = [i.replace('amp;', '') for i in urls]
            # yield urls
            with open(name+'.txt', 'a+', encoding='utf-8') as f:
                for i in urls:
                    url = 'https://www.landchina.com/' + i
                    f.write(url)
                    f.write('\n')
                print('第：{}页url保存成功'.format(num - 1))
            # 页面跳转
            inpu = self.driver.find_element_by_css_selector('a+ input')
            inpu.clear()
            inpu.send_keys(num)
            enter = self.driver.find_elements_by_xpath('//input[contains(@value,"go")]')
            enter[1].click()

        self.driver.quit()

    def get_html(self, file_name):
        count = 1
        try_count = 1
        with open(file_name, 'r') as f:
            for url in f.readlines():
                try:
                    self.driver.get(url)

                    # 判断异常
                    while True:
                        if try_count > 2:
                            print('An error occurred 错误！')
                            self.driver.quit()
                            os._exit(0)
                        if 'An error occurred' in self.driver.page_source:
                            self.driver.refresh()
                            time.sleep(1)
                            try_count += 1
                        try_count = 1
                        break
                    r = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="p1"]'))).text
                    r = r.replace('\n', '').replace(' ', '')
                except:
                    if try_count > 2:
                        self.driver.quit()
                        os._exit(0)
                    print('出错')
                    try_count += 1
                    continue
                # 行政区域
                regions = re.findall(
                    '行政区:(.*?)电子监管号', r)[0]
                # 项目名称
                name = re.findall(r'项目名称:(.*?)项目位置', r)[0]
                # 项目位置
                position = re.findall(r'项目位置:(.*?)面积', r)[0]
                # 土地用途
                use = re.findall(r'土地用途:(.*?)供地方式', r)[0]
                # 行业分类
                sort = re.findall(r'行业分类:(.*?)土地级别', r)[0]
                # 面积(公顷)
                area = re.findall(r'面积(.*?)土地来源', r)[0].replace('(公顷):', '')
                # 供地方式
                mode = re.findall(r'供地方式:(.*?)土地使用年限', r)[0]
                # 土地使用年限
                term = re.findall(r'土地使用年限:(.*?)行业分类', r)[0]
                # 成交价(万元)
                price = re.findall(r'成交价格(.*?)分期支付约定', r)[0].replace('(万元):', '')
                # 约定容积率
                agreement = re.findall(r'约定容积率:(.*?)约定交地时间', r)[0]
                # 合同签订日期
                contract_date = re.findall(r'合同签订日期:(.*?)$', r)[0]
                # 数据获取时间
                t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                url = url.replace('\n', '')
                data = [[regions, name, position, use, sort, area, mode, term, price, agreement, contract_date, url, t]]
                self.sav_data(data)
                print('第：[{}] 条数据保存成功'.format(count))
                count += 1
                # 备份
                shutil.copy(self.file_name, '备份数据.xlsx')
                time.sleep(1.5)

    def sav_data(self, data):
        """
        保存数据
        :return:
        """
        with open(self.file_name, "a+", encoding='utf-8', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open(self.file_name, "r", encoding='utf-8', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(['行政区域', '项目名称', '项目位置', '土地用途', '行业分类', '面积(公顷)', '供地方式', '土地使用年限', '成交价(万元)', '约定容积率', '合同签订日期', '数据来源', '数据写入日期'])
                    k.writerows(data)
                else:
                    k.writerows(data)

    def run(self):
        path = os.getcwd()
        files = os.listdir(path)
        files = [i for i in files if 'txt' in i if '备份数据' not in i]
        print(files)
        for file_name in files:
            print(file_name)
            (filename, extension) = os.path.splitext(file_name)
            self.file_name = filename + '.csv'
            print('新文件名：{}'.format(self.file_name))
            self.get_html(file_name)
            # 移动已处理完文件
            shutil.move(self.file_name, '完成/')
            os.remove(file_name)
            print('文件：{} 保存成功!'.format(self.file_name))


def get_html1():
    from requests_html import HTMLSession
    """
    获取详情页数据
    :return:
    """
    count = 0
    headers = {'User-Agent': str(UserAgent().random),
               'Connection': 'keep-alive',
               'Host': 'www.landchina.com',
               'Cookie': 'security_session_high_verify=e5bbe410c3ec71512f9445aa5febc966; ASP.NET_SessionId=pb2vt2pu3321maauec0fb5un; Hm_lvt_83853859c7247c5b03b527894622d3fa=1598256051,1598259293; security_session_verify=c595ae20ad48407179d8f1063f4b30bb; Hm_lpvt_83853859c7247c5b03b527894622d3fa=1598265089'
               }
    session = HTMLSession()
    with open('四川-招拍挂出让数据.txt', 'r') as f:
        for url in f.readlines():
            # url = 'https://www.landchina.com/default.aspx?tabid=386&comname=default&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&recorderguid=cfef59e5-5e17-460d-8a74-c026017164db'
            # session = HTMLSession()
            print(url)
            r = session.get(url, headers=headers, verify=False)
            print(r.text)
            r = re.findall(r'<div id="p1" style="clear:both;">(.*?)</div></div><script type="text/javascript">', r.text)[0]
            html = etree.HTML(r)
            content = html.xpath('//tr//text()')
            r = ''.join(content)
            # 行政区域
            regions = re.findall(
                '行政区:(.*?)电子监管号', r)[0]
            # 项目名称
            name = re.findall(r'项目名称:(.*?)项目位置', r)[0]
            # 项目位置
            position = re.findall(r'项目位置:(.*?)面积', r)[0]
            # 土地用途
            use = re.findall(r'土地用途:(.*?)供地方式', r)[0]
            # 行业分类
            sort = re.findall(r'行业分类:(.*?)土地级别', r)[0]
            # 面积(公顷)
            area = re.findall(r'面积(.*?)土地来源', r)[0].replace('(公顷):', '')
            # 供地方式
            mode = re.findall(r'供地方式:(.*?)土地使用年限', r)[0]
            # 土地使用年限
            term = re.findall(r'土地使用年限:(.*?)行业分类', r)[0]
            # 成交价(万元)
            price = re.findall(r'成交价格(.*?)分期支付约定', r)[0].replace('(万元):', '')
            # 约定容积率
            agreement = re.findall(r'约定容积率:(.*?)约定交地时间', r)[0]
            # 合同签订日期
            contract_date = re.findall(r'合同签订日期:(.*?)$', r)[0]
            # 数据获取时间
            t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = [[regions, name, position, use, sort, area, mode, term, price, agreement, contract_date, url, t]]
            print(data)
            with open('四川.csv', "a+", encoding='utf-8', newline="") as f:
                k = csv.writer(f, delimiter=',')
                with open('四川.csv', "r", encoding='utf-8', newline="") as f1:
                    reader = csv.reader(f1)
                    if not [row for row in reader]:
                        k.writerow(
                            ['行政区域', '项目名称', '项目位置', '土地用途', '行业分类', '面积(公顷)', '供地方式', '土地使用年限', '成交价(万元)', '约定容积率',
                             '合同签订日期', '数据来源', '数据写入日期'])
                        k.writerows(data)
                    else:
                        k.writerows(data)
            print('第：[{}] 条数据保存成功'.format(count))
            count += 1


if __name__ == '__main__':
    spider = Spider()
    # 获取数据
    spider.run()
    # 获取url
    # spider.get_code()
