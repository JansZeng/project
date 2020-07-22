import re
import os
import csv
import time
import requests
from lxml import etree
from retrying import retry
from fake_useragent import UserAgent


class ShangCheWang(object):
    def __init__(self):
        self.count = 0

    @retry(stop_max_attempt_number=3)
    def _parse_url(self, url):
        """url请求"""
        headers = {"User-Agent": UserAgent().random}
        while True:
            try:
                response = requests.get(url, headers=headers, verify=False, timeout=300)
                if not response.text:
                    continue
            except Exception as e:
                print(e)
                continue
            return response

    def get_notice_list(self):
        """获取所有批次url和批次号"""
        url = 'https://www.cn357.com/notice_list'
        response = self._parse_url(url=url)
        html = etree.HTML(response.text)
        if not html:
            return
        notice_urls = html.xpath('//div[@class="lotList uiLinkList clear"]/a/@href')
        notice_urls = [f'https://www.cn357.com{i}' for i in notice_urls]
        notice_titles = html.xpath('//div[@class="lotList uiLinkList clear"]/a/text()')
        for notice in zip(notice_titles, notice_urls):
            notice_title, notice_url = notice
            yield notice_title, notice_url

    def get_table_list(self, notice_url):
        """获取产品型号 生产企业信息"""
        response = self._parse_url(url=notice_url)
        html = etree.HTML(response.text)
        table_titles = html.xpath('//div[@class="gMain"]/table/tr/td/a/text()')  # 车辆型号
        # 一页60条
        table_urls = html.xpath('//div[@class="gMain"]/table/tr/td/a/@href')  # 车辆详情url
        table_urls = [f'https://www.cn357.com{i}' for i in table_urls]
        table_frims = html.xpath('//div[@class="gMain"]/table/tr/td[2]/text()')  # 生产企业
        for table in zip(table_titles, table_urls, table_frims):
            table_title, table_url, table_frim = table
            yield table_title, table_url, table_frim

    def get_content(self, table_url):
        """获取详细数据"""
        data = {}
        response = self._parse_url(url=table_url)
        html = etree.HTML(response.text)
        content = html.xpath('//table//text()')
        content = '=='.join([i.replace(' ', '').replace('\n', '') for i in content if i.replace(' ', '').replace('\n', '')])
        print(content)
        data['变更(扩展)记录'] = re.findall('变更\(扩展\)记录(.*?)公告型号', content)[0].replace('==', '')
        data['公告型号'] = re.findall('公告型号(.*?)公告批次', content)[0].replace('==', '')
        data['公告批次'] = re.findall('公告批次(.*?)品牌', content)[0].replace('==', '')
        data['品牌'] = re.findall('品牌(.*?)类型', content)[0].replace('==', '')
        data['类型'] = re.findall('类型(.*?)额定质量', content)[0].replace('==', '')
        data['额定质量'] = re.findall('额定质量(.*?)总质量', content)[0].replace('==', '')
        data['总质量'] = re.findall('总质量(.*?)整备质量', content)[0].replace('==', '')
        data['整备质量'] = re.findall('整备质量(.*?)燃料种类', content)[0].replace('==', '')
        data['燃料种类'] = re.findall('燃料种类(.*?)排放依据标准', content)[0].replace('==', '')
        data['排放依据标准'] = re.findall('排放依据标准(.*?)轴数', content)[0].replace('==', '')
        data['轴数'] = re.findall('轴数(.*?)轴距', content)[0].replace('==', '')
        data['轴距'] = re.findall('轴距(.*?)轴荷', content)[0].replace('==', '')
        data['轴荷'] = re.findall('轴荷(.*?)弹簧片数', content)[0].replace('==', '')
        data['弹簧片数'] = re.findall('弹簧片数(.*?)轮胎数', content)[0].replace('==', '')
        data['轮胎数'] = re.findall('轮胎数(.*?)轮胎规格', content)[0].replace('==', '')
        data['轮胎规格'] = re.findall('轮胎规格(.*?)接近离去角', content)[0].replace('==', '')
        data['接近离去角'] = re.findall('接近离去角(.*?)前悬后悬', content)[0].replace('==', '')
        data['前悬后悬'] = re.findall('前悬后悬(.*?)前轮距', content)[0].replace('==', '')
        data['前轮距'] = re.findall('前轮距(.*?)后轮距', content)[0].replace('==', '')
        data['后轮距'] = re.findall('后轮距(.*?)识别代号', content)[0].replace('==', '')
        data['识别代号'] = re.findall('识别代号(.*?)整车长', content)[0].replace('==', '')
        data['整车长'] = re.findall('整车长(.*?)整车宽', content)[0].replace('==', '')
        data['整车宽'] = re.findall('整车宽(.*?)整车高', content)[0].replace('==', '')
        data['整车高'] = re.findall('整车高(.*?)货厢长', content)[0].replace('==', '')
        data['货厢长'] = re.findall('货厢长(.*?)货厢宽', content)[0].replace('==', '')
        data['货厢宽'] = re.findall('货厢宽(.*?)货厢高', content)[0].replace('==', '')
        data['货厢高'] = re.findall('货厢高(.*?)最高车速', content)[0].replace('==', '')
        data['最高车速'] = re.findall('最高车速(.*?)额定载客', content)[0].replace('==', '')
        data['额定载客'] = re.findall('额定载客(.*?)驾驶室准乘人数', content)[0].replace('==', '')
        data['驾驶室准乘人数'] = re.findall('驾驶室准乘人数(.*?)转向形式', content)[0].replace('==', '')
        data['转向形式'] = re.findall('转向形式(.*?)准拖挂车总质量', content)[0].replace('==', '')
        data['准拖挂车总质量'] = re.findall('准拖挂车总质量(.*?)载质量利用系数', content)[0].replace('==', '')
        data['载质量利用系数'] = re.findall('载质量利用系数(.*?)半挂车鞍座最大承载质量', content)[0].replace('==', '')
        data['半挂车鞍座最大承载质量'] = re.findall('半挂车鞍座最大承载质量(.*?)企业名称', content)[0].replace('==', '')
        data['企业名称'] = re.findall('企业名称(.*?)企业地址', content)[0].replace('==', '')
        data['企业地址'] = re.findall('企业地址(.*?)电话号码', content)[0].replace('==', '')
        data['电话号码'] = re.findall('电话号码(.*?)传真号码', content)[0].replace('==', '')
        data['传真号码'] = re.findall('传真号码(.*?)邮政编码', content)[0].replace('==', '')
        data['邮政编码'] = re.findall('邮政编码(.*?)底盘1', content)[0].replace('==', '')
        data['底盘1'] = re.findall('底盘1(.*?)底盘2', content)[0].replace('==', '')
        data['底盘2'] = re.findall('底盘2(.*?)底盘3', content)[0].replace('==', '')
        data['底盘3'] = re.findall('底盘3(.*?)底盘4', content)[0].replace('==', '')
        data['底盘4'] = re.findall('底盘4(.*?)发动机型号', content)[0].replace('==', '') if re.findall('底盘4(.*?)发动机型号', content) else ''
        data['发动机型号'] = ','.join(html.xpath('//td/table/tr[2]/td[1]/text()'))
        data['发动机生产企业'] = ','.join(html.xpath('//td/table/tr[2]/td[2]/text()'))
        data['发动机商标'] = ','.join(html.xpath('//td/table/tr[2]/td[3]/text()'))
        data['排量'] = ','.join(html.xpath('//td/table/tr[2]/td[4]/text()'))
        data['功率'] = ','.join(html.xpath('//td/table/tr[2]/td[5]/text()'))
        data['备注'] = re.findall('备注(.*?)$', content)[0].replace('==', '')
        return data

    def sav_data(self, data):
        """
        保存数据
        :return:
        """
        with open('data.csv', "a+", encoding='utf-8', newline="") as f:
            k = csv.writer(f, delimiter=',')
            with open('data.csv', "r", encoding='utf-8', newline="") as f1:
                reader = csv.reader(f1)
                if not [row for row in reader]:
                    k.writerow(
                        ['批次号', '产品型号', '生产企业', '变更(扩展)记录', '公告型号', '公告批次', '品牌', '类型', '额定质量', '总质量', '整备质量', '燃料种类', '排放依据标准',
                         '轴数', '轴距', '轴荷', '弹簧片数', '轮胎数', '轮胎规格', '接近离去角', '前悬后悬', '前轮距', '后轮距',
                         '识别代号', '整车长', '整车宽', '整车高', '货厢长', '货厢宽', '货厢高', '最高车速', '额定载客', '驾驶室准乘人数',
                         '转向形式', '准拖挂车总质量', '载质量利用系数', '半挂车鞍座最大承载质量', '企业名称', '企业地址', '电话号码', '传真号码', '邮政编码',
                         '底盘1', '底盘2', '底盘3', '底盘4', '发动机型号', '发动机生产企业', '发动机商标', '排量', '功率', '备注'
                         ])
                    k.writerows(data)
                else:
                    k.writerows(data)
            self.count += 1
            print(f'成功插入第：{self.count}条数据')

    def keep_records(self, table_url, vali=False):
        """保存获取记录"""
        file_name = '获取记录.txt'
        if not os.path.exists(file_name):
            fi = open(file_name, 'a')
            fi.close()
        if vali:
            with open(file_name, 'r') as f:
                flight = [i.replace('\n', '') for i in f.readlines()]
                if table_url in flight:
                    return True
                return False
        else:
            with open(file_name, 'a+') as f:
                f.write(table_url)
                f.write('\n')

    def run(self):
        # 获取所有批次url和批次号
        for notice_title, notice_url in self.get_notice_list():
            # 获取产品型号 生产企业信息
            for table_title, table_url, table_frim in self.get_table_list(notice_url=notice_url):
                if self.keep_records(str(table_url), vali=True):
                    print(f'{table_url} 已获取跳过!')
                    continue
                print(table_url)
                # 获取车辆详细信息
                data = self.get_content(table_url=table_url)
                new_data = [notice_title, table_title, table_frim]
                for i in data.values():
                    new_data.append(i)
                self.sav_data(data=[new_data])
                if self.count > 50:
                    return
                time.sleep(1)
                self.keep_records(table_url)


if __name__ == '__main__':
    spider = ShangCheWang()
    spider.run()
    spider.get_content(table_url='https://www.cn357.com/notice884200_SC6955XCG5')
