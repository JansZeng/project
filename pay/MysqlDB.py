# coding=utf-8
# 作者    ： Administrator
# 文件    ：Sqlite_Demo.py
# IED    ：PyCharm
# 创建时间 ：2020/6/3 19:19
import pymysql


class DBTool(object):
    def __init__(self):
        db_config = {
            # 'host': '*******',
            'host': '*********',
            'port': 3306,
            'user': 'pay',
            'password': 'pay123456',
            'db': 'pay',
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
                    # print('数据类型错误')
                    return
            if count > 0:
                # 返回插入数据数量
                # print('成功写入{0}条数据'.format(count))
                # 提交数据库事务
                self.conn.commit()
                return count
            return False
        except pymysql.DatabaseError as e:
            # 回滚数据库事物
            self.conn.rollback()
            print('插入数据失败:{}'.format(e))

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

    def close(self):
        """
        关闭数据库
        """
        self.conn.close()
        self.cursor.close()


if __name__ == '__main__':
    print('查询数据')
    db = DBTool()
    # 查询
    c_sql = 'SELECT * FROM sms'
    # 插入数据 卡号，到账信息，金额，到账时间，写入时间
    data = ('1111', '成功入账了二次', '20', '2020-08-06 01:00:00', '1596431111')
    print(data)
    sql = """INSERT INTO sms(bankcard_num,sms_content,fee,pay_time,create_time) VALUES (%s,%s,%s,%s,%s)"""
    a = db.create(sql, data)  # 数据写入
    b = db.query(sql=c_sql)
    print(a)
    print(b)