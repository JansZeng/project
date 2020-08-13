# -*- coding:utf-8 -*-
# 作者    ： cenjy
# 文件    ：Sqlite_Demo.py
# IED    ：PyCharm
# 创建时间 ：2020/6/3 19:19
"""
读取猫池mdb数据库数据，写入服务器mysql数据库

10秒读取一次
"""
import re
import time
import os
import sys
import logging
import datetime
from MysqlDB import DBTool
from AccessDB import AccessMdb


PATH = os.getcwd()


def run_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.datetime.now()
        log_init().info("程序开始时间：{}".format(start_time))
        res = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        log_init().info("程序结束时间：{}".format(end_time))
        log_init().info("程序执行用时：{}s".format((end_time - start_time)))
        log_init().info('*'*20)
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


def query_mdb():
    """第一步：查询mdb数据库中最新数据"""
    # 初始化MDB数据库连接
    db_name = r'D:\kuwangtong\Data\SMS.mdb'  # 文件名
    password = 'gd2013'  # 数据库密码
    tablename = 'L_SMS'  # 表名
    accessMdb = AccessMdb(db_name=db_name, password=password)  # 数据库连接
    # 查询mdb数据库中最新的10条数据
    # print('查询mdb数据库数据')
    # sql = f"SELECT content,time,simnum FROM {tablename} where pcui = 38"
    # select top 5 * from {tablename} order by id desc; ：倒序查询最后100条数据
    # sql = f"SELECT content,time,simnum FROM (select top 100 * from {tablename} order by id desc)"

    # 根据di倒序查询最后十条数据
    sql = f"SELECT content,time,simnum FROM (select top 10 * from {tablename} order by id desc)"
    data = accessMdb.mdb_sel(sql)
    log_init().info(f'MDB数据库查询到{len(data)}条数据。')
    return data


def filter_data(data):
    """
    第二步：筛选符合条件的数据
    条件一：当天数据
    条件二：最近十分钟数据
    """
    # 定义当天时间
    new_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '0:00:00', '%Y-%m-%d%H:%M:%S')
    # 当前时间-10分钟
    # new_time = datetime.datetime.strptime((datetime.datetime.now() - datetime.timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')

    # 判断规定时间内是否接收到新短信
    data = [i for i in data if datetime.datetime.strptime(i[1], '%Y-%m-%d %H:%M:%S') > new_time]
    if not data:
        log_init().info('没有接收到新信息！')
        return None
    return data


def process_sms(new_data):
    """第三步：数据处理 到账短信"""
    content = new_data[0]
    # 卡号
    bankcard = re.findall(r'[尾号|为|账户](\d+)', content)
    bankcard = bankcard[0] if bankcard else ''

    # 金额
    fee = re.findall(r'[转|存|汇|入人民币](\d+)', content)
    fee = int(fee[0]) * 100 if fee else 0

    # 到账信息余额替换***
    balance = re.findall(r'[余额](.*?)元', content)
    if balance:
        sms_content = content.replace(balance[0], '****')
    else:
        sms_content = content
    if not bankcard or not fee:
        return None
    # 卡号， 到账信息， 金额， 到账时间， 手机号，写入时间
    sms_data = (bankcard, sms_content, fee, new_data[1], new_data[2], int(time.time()))
    return sms_data


def process_code(new_data):
    """第三步：数据处理 验证码短信"""
    content = new_data[0]
    # 验证码
    code_content = re.findall(r'[验证码](\d+)', content)
    if not code_content:
        return None
    # 手机号码， 短信内容， 验证码， 时间
    code_data = (new_data[2], new_data[0], code_content[0], new_data[1])
    return code_data


def create_sms(sqliteDB, sms_data):
    """第四步：写入到账信息"""
    log_init().info('写入到账信息')
    count = 0  # 写入计数
    for sms in sms_data:
        # 插入数据前判断数据库中是否有这条数据，解决id混乱问题
        s_sql = f"""select * from sms where sms_content = '{sms[1]}' and pay_time = '{sms[3]}'"""
        if sqliteDB.query(s_sql):
            # print('重复数据跳过')
            continue

        # 插入数据
        c_sql = """INSERT ignore INTO sms(bankcard_num,sms_content,fee,pay_time,phone,create_time) VALUES (%s,%s,%s,%s,%s,%s)"""
        res = sqliteDB.create(c_sql, sms)
        if res:
            count += 1
    if not count:
        log_init().info('数据重复，没有新信息！')
        return
    log_init().info(f'成功写入：{count} 条数据')


def create_code(sqliteDB, code_data):
    """第四步：写入验证码短信"""
    log_init().info('写入验证码短信')

    count = 0  # 写入计数
    for code in code_data:
        # 插入数据前判断数据库中是否有这条数据，解决id混乱问题
        s_sql = f"""select * from code where code_content = '{code[1]}' and code_time = '{code[3]}'"""
        if sqliteDB.query(s_sql):
            # print('重复数据跳过')
            continue

        # 插入数据
        c_sql = """INSERT ignore INTO code(phone,code_content,code,code_time) VALUES (%s,%s,%s,%s)"""
        res = sqliteDB.create(c_sql, code)
        if res:
            count += 1
    if not count:
        log_init().info('数据重复，没有新信息！')
        return
    log_init().info(f'成功写入：{count} 条数据')


def run():
    while True:
        try:
            # 第一步：查询mdb数据库最新数据
            data = query_mdb()

            # 第二步：筛选符合条件的数据，十分钟内接收到的新信息
            new_data = filter_data(data=data)

            # 第三步：匹配最新信息是否为到账信息或者验证码信息
            sms_data = [process_sms(new_data=i) for i in new_data if process_sms(new_data=i)]  # 正则匹配是否为到账信息
            code_data = [process_code(new_data=i) for i in new_data if process_code(new_data=i)]  # 正则匹配是否为验证码信息
            if not sms_data and not code_data:  # 没有匹配到数据，终止程序
                return

            # 第四步：最新信息写入线上数据库
            log_init().info('连接数据库...')
            sqliteDB = DBTool()  # 初始化mysql数据库连接
            log_init().info('连接数据库成功,数据写入中...')
            if sms_data:
                create_sms(sqliteDB=sqliteDB, sms_data=sms_data)
            if code_data:
                create_code(sqliteDB=sqliteDB, code_data=code_data)

            # 关闭数据库连接
            log_init().info('数据写入完毕，关闭数据库连接!')
            sqliteDB.close()
        except Exception as e:
            log_init().error(e)
            log_init().error('运行错误，联系开发者')
        finally:
            time.sleep(10000)


if __name__ == '__main__':
    run()

