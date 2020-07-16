# coding=utf-8
# 作者    ： Administrator
# 文件    ：Sqlite_Demo.py
# IED    ：PyCharm
# 创建时间 ：2020/6/3 19:19
import sqlite3


class DBTool(object):
    def __init__(self, filename="sms"):
        """
        初始化数据库，默认文件名 stsql.db
        filename：文件名
        """
        # 创建数据库 不存在时在py同一目录下自动创建test.db
        self.filename = filename + ".db"
        self.conn = sqlite3.connect(self.filename)
        # 创建游标
        self.cursor = self.conn.cursor()
        # 创建表
        self.connect_db()

    def connect_db(self):
        """创建表 不存在则创建"""
        # 创建test表:判断表是否存在,存在则跳过,不存在创建
        test_sql = "select count(*)  from sqlite_master where type='table' and name = 'sim_content';"
        test_cur = self.cursor.execute(test_sql)

        if not test_cur.fetchone()[0]:
            self.cursor.execute(
                """create table if not EXISTS sim_content
                  ('Id' integer primary key,
                  'Content' varchar(255),
                  'time' timestamp(6),
                  'Simnum' varchar(255),
                  'Md5' varchar(255))""")

            print('sim_content 表创建成功!')

    def close(self):
        """
        关闭数据库
        """
        self.conn.close()
        self.cursor.close()

    def execute(self, sql, param=None):
        """
        执行数据库的增、删、改
        sql：sql语句
        param：数据，可以是list或tuple，亦可是None
        retutn：成功返回True
        """
        try:
            if param is None:
                self.cursor.execute(sql)
            else:
                if type(param) is list:
                    self.cursor.executemany(sql, param)
                elif type(param) is tuple:
                    self.cursor.execute(sql, param)
                else:
                    print('数据类型错误')
                    return
            # 返回插入数据数量
            count = self.conn.total_changes
        except Exception as e:
            print(e)
            return False, e
        finally:
            # 提交事务
            self.conn.commit()
        if count > 0:
            return count
        else:
            return False

    def query(self, sql, param=None):
        """
        查询语句
        sql：sql语句
        param：参数,可为None
        retutn：成功返回True
        """
        if param is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, param)
        return self.cursor.fetchall()


if __name__ == '__main__':
    sqlite_sql = """INSERT INTO sim_content ('Content', 'time', 'Simnum', 'Md5') VALUES (?,?,?,?)"""
    # data = 列表或者元祖
    data = [('【咪咕阅读】钜惠来袭~0元享海量至臻听书VIP，名家朗读、无损音质！宅家、出行不无聊，精选内容放肆听→ http://u.cmread', '2020-07-15 17:37:34', '18210836362', '123')]
    # 连接数据库
    db = DBTool()
    print('插入数据')
    # i = db.execute(sql=sqlite_sql, param=data)
    # print(f'成功插入{i}条数据')
    print('查询数据')
    # 查询
    sql = 'SELECT Md5 FROM sim_content'
    a = db.query(sql=sql)
    print(a)