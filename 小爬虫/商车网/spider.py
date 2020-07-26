"""
mysql==5.7.26
"""
import re
import os
import csv
import time
import pinyin
import hashlib
import pymysql
import requests
from lxml import etree
from retrying import retry
from fake_useragent import UserAgent
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ShangCheWang(object):
    def __init__(self):
        self.count = 0

    @retry(stop_max_attempt_number=10)
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
        while True:
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

            # 获取下一页url
            print('翻页')
            next_url = html.xpath('//a[contains(text(), "下一页")]/@href')
            if not next_url:
                break
            notice_url = f'https://www.cn357.com{next_url[0]}'

    def get_content(self, table_url):
        """获取详细数据"""
        data = {}
        response = self._parse_url(url=table_url)
        html = etree.HTML(response.text)
        content = html.xpath('//table//text()')
        content = '=='.join([i.replace(' ', '').replace('\n', '') for i in content if i.replace(' ', '').replace('\n', '')])
        if not content:
            return False
        # print(content)
        # data['变更(扩展)记录'] = re.findall('变更\(扩展\)记录(.*?)公告型号', content)[0].replace('==', '')
        # data['公告型号'] = re.findall('公告型号(.*?)公告批次', content)[0].replace('==', '')
        # data['公告批次'] = re.findall('公告批次(.*?)品牌', content)[0].replace('==', '')
        # data['品牌'] = re.findall('品牌(.*?)类型', content)[0].replace('==', '')
        # data['类型'] = re.findall('类型(.*?)额定质量', content)[0].replace('==', '')
        # data['额定质量'] = re.findall('额定质量(.*?)总质量', content)[0].replace('==', '')
        # data['总质量'] = re.findall('总质量(.*?)整备质量', content)[0].replace('==', '')
        # data['整备质量'] = re.findall('整备质量(.*?)燃料种类', content)[0].replace('==', '')
        # data['燃料种类'] = re.findall('燃料种类(.*?)排放依据标准', content)[0].replace('==', '')
        # data['排放依据标准'] = re.findall('排放依据标准(.*?)轴数', content)[0].replace('==', '')
        # data['轴数'] = re.findall('轴数(.*?)轴距', content)[0].replace('==', '')
        # data['轴距'] = re.findall('轴距(.*?)轴荷', content)[0].replace('==', '')
        # data['轴荷'] = re.findall('轴荷(.*?)弹簧片数', content)[0].replace('==', '')
        # data['弹簧片数'] = re.findall('弹簧片数(.*?)轮胎数', content)[0].replace('==', '')
        # data['轮胎数'] = re.findall('轮胎数(.*?)轮胎规格', content)[0].replace('==', '')
        # data['轮胎规格'] = re.findall('轮胎规格(.*?)接近离去角', content)[0].replace('==', '')
        # data['接近离去角'] = re.findall('接近离去角(.*?)前悬后悬', content)[0].replace('==', '')
        # data['前悬后悬'] = re.findall('前悬后悬(.*?)前轮距', content)[0].replace('==', '')
        # data['前轮距'] = re.findall('前轮距(.*?)后轮距', content)[0].replace('==', '')
        # data['后轮距'] = re.findall('后轮距(.*?)识别代号', content)[0].replace('==', '')
        # data['识别代号'] = re.findall('识别代号(.*?)整车长', content)[0].replace('==', '')
        # data['整车长'] = re.findall('整车长(.*?)整车宽', content)[0].replace('==', '')
        # data['整车宽'] = re.findall('整车宽(.*?)整车高', content)[0].replace('==', '')
        # data['整车高'] = re.findall('整车高(.*?)货厢长', content)[0].replace('==', '')
        # data['货厢长'] = re.findall('货厢长(.*?)货厢宽', content)[0].replace('==', '')
        # data['货厢宽'] = re.findall('货厢宽(.*?)货厢高', content)[0].replace('==', '')
        # data['货厢高'] = re.findall('货厢高(.*?)最高车速', content)[0].replace('==', '')
        # data['最高车速'] = re.findall('最高车速(.*?)额定载客', content)[0].replace('==', '')
        # data['额定载客'] = re.findall('额定载客(.*?)驾驶室准乘人数', content)[0].replace('==', '')
        # data['驾驶室准乘人数'] = re.findall('驾驶室准乘人数(.*?)转向形式', content)[0].replace('==', '')
        # data['转向形式'] = re.findall('转向形式(.*?)准拖挂车总质量', content)[0].replace('==', '')
        # data['准拖挂车总质量'] = re.findall('准拖挂车总质量(.*?)载质量利用系数', content)[0].replace('==', '')
        # data['载质量利用系数'] = re.findall('载质量利用系数(.*?)半挂车鞍座最大承载质量', content)[0].replace('==', '')
        # data['半挂车鞍座最大承载质量'] = re.findall('半挂车鞍座最大承载质量(.*?)企业名称', content)[0].replace('==', '')
        # data['企业名称'] = re.findall('企业名称(.*?)企业地址', content)[0].replace('==', '')
        # data['企业地址'] = re.findall('企业地址(.*?)电话号码', content)[0].replace('==', '')
        # data['电话号码'] = re.findall('电话号码(.*?)传真号码', content)[0].replace('==', '')
        # data['传真号码'] = re.findall('传真号码(.*?)邮政编码', content)[0].replace('==', '')
        # data['邮政编码'] = re.findall('邮政编码(.*?)底盘1', content)[0].replace('==', '')
        # data['底盘1'] = re.findall('底盘1(.*?)底盘2', content)[0].replace('==', '')
        # data['底盘2'] = re.findall('底盘2(.*?)底盘3', content)[0].replace('==', '')
        # data['底盘3'] = re.findall('底盘3(.*?)底盘4', content)[0].replace('==', '')
        # data['底盘4'] = re.findall('底盘4(.*?)发动机型号', content)[0].replace('==', '') if re.findall('底盘4(.*?)发动机型号', content) else ''
        # data['发动机型号'] = ','.join(html.xpath('//td/table/tr[2]/td[1]/text()'))
        # data['发动机生产企业'] = ','.join(html.xpath('//td/table/tr[2]/td[2]/text()'))
        # data['发动机商标'] = ','.join(html.xpath('//td/table/tr[2]/td[3]/text()'))
        # data['排量'] = ','.join(html.xpath('//td/table/tr[2]/td[4]/text()'))
        # data['功率'] = ','.join(html.xpath('//td/table/tr[2]/td[5]/text()'))
        # data['备注'] = re.findall('备注(.*?)$', content)[0].replace('==', '')
        data['生产企业'] = ''
        data['公告型号'] = re.findall('公告型号(.*?)公告批次', content)[0].replace('==', '')
        data['公告批次'] = re.findall('公告批次(.*?)品牌', content)[0].replace('==', '')
        data['品牌'] = re.findall('品牌(.*?)类型', content)[0].replace('==', '').split('(')[0]
        data['类型'] = re.findall('类型(.*?)额定质量', content)[0].replace('==', '')
        data['燃料种类'] = re.findall('燃料种类(.*?)排放依据标准', content)[0].replace('==', '')
        data['轴数'] = re.findall('轴数(.*?)轴距', content)[0].replace('==', '')
        data['轴距'] = re.findall('轴距(.*?)轴荷', content)[0].replace('==', '')
        data['识别代号'] = re.findall('识别代号(.*?)整车长', content)[0].replace('==', '')
        data['整车长'] = re.findall('整车长(.*?)整车宽', content)[0].replace('==', '').replace('/', ',')
        data['整车宽'] = re.findall('整车宽(.*?)整车高', content)[0].replace('==', '').replace('/', ',')
        data['整车高'] = re.findall('整车高(.*?)货厢长', content)[0].replace('==', '').replace('/', ',')
        data['发动机型号'] = ','.join(html.xpath('//td/table/tr[2]/td[1]/text()'))

        return data

    def processing(self, data):
        """数据处理"""
        # 过滤类型
        with open('vehicle_type.txt', 'r', encoding='gbk') as f:
            vars = [i.replace('\n', '') for i in f.readlines() if i]
            if data['类型'] not in vars:
                print(f'类型：{data["类型"]} 不在文件中，跳过。')
                return False

        # 只保留轴数为2的数据
        try:
            if int(data['轴数']) != 2:
                print(f'轴数:{data["轴数"]} 跳过')
                return False
        except:
            print(f'轴数:{data["轴数"]} 跳过')
            return False

        # 有识别代号 入库，没有跳过，一行一条，取前8位
        if not data['识别代号']:
            print('没有识别代号跳过')
            return False
        vin = list(set([i[:8] for i in data['识别代号'].split(',')]))  # 取前八位，去重

        # 轴距  长  宽  高   只取第一个数据 +品牌 计算md5
        md5data = str(data['轴距']) + str(data['整车长'].split(',')[0]) + str(data['整车宽'].split(',')[0]) + str(data['整车高'].split(',')[0] + data['品牌'])
        mdbMd5 = self.updateMd5(md5data)
        data['MD5'] = mdbMd5
        for i in vin:
            data['识别代号'] = i
            yield data

    def updateMd5(self, data):
        # 创建md5对象
        md5obj = hashlib.md5()
        md5obj.update(data.encode(encoding='utf-8'))
        md5code = md5obj.hexdigest()
        return md5code

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

    def keep_records(self, table_url, file_name, vali=False):
        """保存获取记录"""
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
            # 效验批次
            if self.keep_records(table_url=str(notice_title), file_name='获取批次记录.txt', vali=True):
                print(f'{notice_title} 已获取跳过!')
                continue
            # 获取产品型号 生产企业信息
            for table_title, table_url, table_frim in self.get_table_list(notice_url=notice_url):
                if self.keep_records(table_url=str(table_url), file_name='获取记录.txt', vali=True):
                    print(f'{table_url} 已获取跳过!')
                    continue
                print(f'{notice_title} {table_title} {table_url} 数据获取中...')
                # 获取车辆详细信息
                data = self.get_content(table_url=table_url)
                if not data:
                    continue
                data['生产企业'] = table_frim
                brand_name = data['品牌']
                for i in spider.processing(data):
                    # 创建数据库连接  入库
                    db = MySql()
                    # 公告型号+识别代号 去重
                    sql_b = "select vehicle_model_code,vin from cndatebase WHERE vehicle_model_code='{}' and vin='{}'".format(data['公告型号'], data['识别代号'])
                    if db.query(sql=sql_b):
                        print('公告型号+识别代号 去重 数据重复跳过。')
                        continue
                    # 查询 cnial表品牌名称对应id
                    sql_a = "SELECT id FROM cnial WHERE brand_name='{}';".format(brand_name)
                    param = (brand_name, pinyin.get(brand_name).capitalize()[0])
                    brand_name_id = db.query(sql_a, param=param)[0]
                    data['品牌'] = brand_name_id[0]
                    # 插入数据
                    sql = "INSERT INTO cndatebase(producer, vehicle_model_code, batch, brand_name, vehicle_type, fuel_type, axes_num, wheel_base, vin, vehicle_length, vehicle_wide, vehicle_high, engine_type, md5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    db.create(sql, tuple(i.values()))
                # new_data = [notice_title, table_title, table_frim]
                # for i in data.values():
                #     new_data.append(i)
                # self.sav_data(data=[new_data])
                # if self.count > 50:
                #     return
                time.sleep(1)
                self.keep_records(table_url=table_url, file_name='获取记录.txt')
            # 记录批次
            self.keep_records(table_url=notice_title, file_name='获取批次记录.txt')


class MySql:
    def __init__(self):
        db_config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'db': 'cn357',
            'charset': 'utf8'
        }
        """获取连接对象和执行对象"""
        self.conn = pymysql.connect(**db_config)
        self.cursor = self.conn.cursor()

    def create(self, sql, content):
        """数据写入"""
        try:
            affectedcount = self.cursor.execute(sql, content)

            # 提交数据库事务
            self.conn.commit()
            print('成功插入{0}条数据'.format(affectedcount))
        except pymysql.DatabaseError as e:
            # 回滚数据库事物
            self.conn.rollback()
            print('插入数据失败:{}'.format(e))
        finally:
            # 关闭数据连接
            self.cursor.close()
            self.conn.close()

    def query(self, sql, param=None):
        """
        查询语句
        sql：sql语句
        param：参数,可为None
        retutn：成功返回True
        """

        self.cursor.execute(sql)
        one = self.cursor.fetchall()
        if not one and param:
            _sql = "INSERT INTO cnial(brand_name, initial) VALUES (%s, %s);"
            self.cursor.execute(_sql, param)
            # 提交数据库事务
            self.conn.commit()
            self.cursor.execute(sql)
            one = self.cursor.fetchall()
        return one


if __name__ == '__main__':
    spider = ShangCheWang()
    spider.run()
    # data = spider.get_content(table_url='https://www.cn357.com/notice835515_JQ9402TJZ')
    # print(data)
    # for i in spider.processing(data):
    #     print(tuple(i.values()), type(tuple(i.values())))
    #     db = MySql()
    #     db.create(tuple(i.values()))

