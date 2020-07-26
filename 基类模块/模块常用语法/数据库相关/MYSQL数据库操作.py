# -*- coding:utf-8 -*-
# 文件 ：script.py
# IED ：PyCharm
# 时间 ：2019/11/22 0022 12:33
# 版本 ：V1.0

import pymysql


class MySql:
    def __init__(self):
        db_config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'db': 'test',
            'charset': 'utf8'
        }
        """获取连接对象和执行对象"""
        self.conn = pymysql.connect(**db_config)
        self.cursor = self.conn.cursor()

    def create(self, sql, param=None):
        """数据写入
        content：元祖
        """
        try:
            if param is None:
                count = self.cursor.execute(sql)
            else:
                if type(param) is list:
                    count = self.cursor.executemany(sql, param)
                elif type(param) is tuple:
                    count = self.cursor.execute(sql, param)
                else:
                    print('数据类型错误')
                    return
            if count > 0:
                # 返回插入数据数量
                # print('成功更新{0}条数据'.format(count))
                # 提交数据库事务
                self.conn.commit()
                return count
            return False
        except pymysql.DatabaseError as e:
            # 回滚数据库事物
            self.conn.rollback()
            print('插入数据失败:{}'.format(e))
        # finally:
        #     # 关闭数据连接
        #     self.cursor.close()
        #     self.conn.close()

    def query(self, sql, param=None):
        """
        查询语句
        sql：sql语句
        param：参数,可为None
        retutn：成功返回True
        """
        try:
            self.cursor.execute(sql)
            fetchall = self.cursor.fetchall()
            return fetchall
        except Exception as e:
            print('查询数据失败:{}'.format(e))