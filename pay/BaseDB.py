# -*- coding:utf-8 -*-
# 作者    ： cenjy
# 文件    ：Sqlite_Demo.py
# IED    ：PyCharm
# 创建时间 ：2020/6/3 19:19
"""
读取猫池mdb数据库数据，写入服务器mysql数据库
"""

from MysqlDB import DBTool
from AccessDB import AccessMdb

# 初始化sqlite数据库连接
sqliteDB = DBTool()
# 初始化MDB数据库连接
db_name = r'D:\kuwangtong\Data\SMS.mdb'  # 文件名
password = 'gd2013'  # 数据库密码
tablename = 'L_SMS'  # 表名

accessMdb = AccessMdb(db_name=db_name, password=password)


def db():
    """数据库操作"""
    # 查询mdb数据库中最新的10条数据
    print('查询mdb数据库数据')
    # sql = f"SELECT content,time,simnum FROM {tablename} where pcui = 38"
    # select top 5 * from {tablename} order by id desc; ：倒序查询最后五条数据
    sql = f"SELECT content,time,simnum FROM (select top 10 * from {tablename} order by id desc) where pcui = 38"
    sel_data = accessMdb.mdb_sel(sql)
    print(f'MDB数据库查询到{len(sel_data)}条数据。')

    for data in sel_data:
        # 向mysql数据库插入数据
        print(data)
        # print(f'成功写入第：{i}条数据')


if __name__ == '__main__':
    db()