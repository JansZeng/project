from django.test import TestCase

# Create your tests here.
import requests
import os
import hashlib
import datetime
from AccessMdb import AccessMdb


def run_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.datetime.now()
        # print("程序开始时间：{}".format(start_time))
        # log_init().info("程序开始时间：{}".format(start_time))
        res = func(*args, **kwargs)
        end_time = datetime.datetime.now()
        print("程序结束时间：{}".format(end_time))
        print("程序执行用时：{}s".format((end_time - start_time)))
        # log_init().info("程序结束时间：{}".format(end_time))
        # log_init().info("程序执行用时：{}s".format((end_time - start_time)))
        return res

    return new_func


def updateMd5(data):
    # 创建md5对象
    md5obj = hashlib.md5()
    md5obj.update(data.encode(encoding='utf-8'))
    md5code = md5obj.hexdigest()
    return md5code


def db():
    """数据库操作"""
    # 初始化MDB数据库连接
    db_name = r'D:\kuwangtong\Data\SMS.mdb'  # 文件名
    password = 'gd2013'  # 数据库密码
    tablename = 'L_SMS'  # 表名
    accessMdb = AccessMdb(db_name=db_name, password=password)

    # 查询mdb数据库中最新的10条数据
    # print('查询mdb数据库数据')
    # sql = f"SELECT content,time,simnum FROM {tablename} where pcui = 38"
    # select top 5 * from {tablename} order by id desc; ：倒序查询最后五条数据
    sql = f"SELECT number, content,time,simnum FROM (select top 10 * from {tablename} order by id desc) where pcui = 38"
    sel_datas = accessMdb.mdb_sel(sql)
    print(f'MDB数据库查询到{len(sel_datas)}条数据。')
    return sel_datas


@run_time
def upload(datas):
    """向服务器上传数据"""
    _url = f'http://www.ccccc.run/sim_update/'
    # _url = f'http://127.0.0.1:8000/sim_update/'
    for da in datas:
        md5 = tuple([updateMd5(da[1])])  # 短信内容转换成md5并转为元祖
        number, content, time, simnum = da
        data = {'number': number, 'content': content, 'time': time, 'simnum': simnum, 'md5': md5}
        print(data.get('content'))
        response = requests.post(_url, data=data)
        print(response.text)
        content = response.json()
        code = content['errorcode']
        if code != 10001:
            os._exit(0)
        try:
            content = response.json()
            code = content['errorcode']
            if code != 10001:
                os._exit(0)
        except Exception as e:
            print('连接服务器错误!')
            print(e)


if __name__ == '__main__':
    # start_time = datetime.datetime.now()
    # print("程序开始时间：{}".format(start_time))
    # # log_init().info("程序开始时间：{}".format(start_time))
    # upload('智能航班】IP账号：ba618b3e3adc4e7c93127546d02a5 即将到期及时续费!', '2020-07-15 17:37:34', '362', '2')
    # end_time = datetime.datetime.now()
    # print("程序结束时间：{}".format(end_time))
    # print("程序执行用时：{}s".format((end_time - start_time)))
    datas = db()
    if datas:
        upload(datas=datas)