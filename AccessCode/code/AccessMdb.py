# -*- coding:utf-8 -*-
# 读取access MDB 文件
"""
常见问题及解决办法：
问题：
1.驱动错误
解决：确定Access版本 和 python版本对应（64位-64位）（32位-32位）
    查看驱动程序是否安装： 控制面板--系统和安全--管理工具--ODBC数据库--驱动程序
    驱动下载：链接：https://pan.baidu.com/s/19YV3XtYpjMmDxQuI7X3APA
            提取码：aoqb
2.[Microsoft][ODBC Microsoft Access Driver]常见错误 无法打开注册表项“Temporary
解决：https://blog.csdn.net/ooooooobh/article/details/52263985
    重新设置了下数据库所在相关目录对于任何用户都是完全控制
"""

__author__ = 'mayi'


# 导入模块
import pypyodbc


class AccessMdb(object):
    def __init__(self, db_name, password=""):
        """
        功能：创建数据库连接
        :param db_name: 数据库名称
        :param db_name: 数据库密码，默认为空
        :return: 返回数据库连接
        """
        str = 'Driver={Microsoft Access Driver (*.mdb)};PWD=' + password + ";DBQ=" + db_name
        self.conn = pypyodbc.win_connect_mdb(str)  # 创建数据库连接
        self.cur = self.conn.cursor()  # 创建游标

    def mdb_add(self, sql):
        """
        功能：向数据库插入数据
        :param conn: 数据库连接
        :param cur: 游标
        :param sql: sql语句
        :return: sql语句是否执行成功
        """
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except:
            return False

    def mdb_del(self, sql):
        """
        功能：向数据库删除数据
        :param conn: 数据库连接
        :param cur: 游标
        :param sql: sql语句
        :return: sql语句是否执行成功
        """
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except:
            return False

    def mdb_modi(self, sql):
        """
        功能：向数据库修改数据
        :param conn: 数据库连接
        :param cur: 游标
        :param sql: sql语句
        :return: sql语句是否执行成功
        """
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return True
        except:
            return False

    def mdb_sel(self, sql):
        """
        功能：向数据库查询数据
        :param cur: 游标
        :param sql: sql语句
        :return: 查询结果集
        """
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except:
            return []





# if __name__ == '__main__':
    # 打印数据库中的所有表的表名
    # print('打印mdb数据库中的所有表的表名')
    # for table_info in cur.tables(tableType='TABLE'):
    #     print(table_info[2])
    # # 读取表头
    # print('读取表头')
    # for col in cur.description:
    #     print(col)
    #     print(col[0], col[1])


    # 增
    # sql = "Insert Into " + tablename + " Values (33, 12, '天津', 0)"
    # if mdb_add(conn, cur, sql):
    #     print("插入成功！")
    # else:
    #     print("插入失败！")
    #
    # # 删
    # sql = "Delete * FROM " + tablename + " where id = 32"
    # if mdb_del(conn, cur, sql):
    #     print("删除成功！")
    # else:
    #     print("删除失败！")
    #
    # # 改
    # sql = "Update " + tablename + " Set IsFullName = 1 where ID = 33"
    # if mdb_modi(conn, cur, sql):
    #     print("修改成功！")
    # else:
    #     print("修改失败！")
    #

    #
    # # 提交数据（只有提交之后，所有的操作才会对实际的物理表格产生影响）
    # cur.commit()  # 提交数据
    # cur.close()  # 关闭游标
    # conn.close()  # 关闭数据库连接