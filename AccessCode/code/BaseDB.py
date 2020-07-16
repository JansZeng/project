import hashlib
from SqliteDatabase import DBTool
from AccessMdb import AccessMdb

# 初始化sqlite数据库连接
sqliteDB = DBTool()
# 初始化MDB数据库连接
db_name = r'D:\kuwangtong\Data\SMS.mdb'  # 文件名
password = 'gd2013'  # 数据库密码
tablename = 'L_SMS'  # 表名

accessMdb = AccessMdb(db_name=db_name, password=password)


def updateMd5(data):
    # 创建md5对象
    md5obj = hashlib.md5()
    md5obj.update(data.encode(encoding='utf-8'))
    md5code = md5obj.hexdigest()
    return md5code


def sqliteDB_query():
    """查询十条最新sqlite数据库短信"""
    sqlite_query_sql = """SELECT Md5 FROM "sim_content" LIMIT 10"""
    # 查询sqlite最新的五条数据 和 mdb数据库对比是否有新数据
    query_contents = sqliteDB.query(sql=sqlite_query_sql)
    query_contents = [i[0] for i in query_contents]
    return query_contents


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
        mdbMd5 = tuple([updateMd5(data[0])])  # 短信内容转换成md5并转为元祖
        # 判断是否有新短信，如果有就写入服务器数据库中
        if mdbMd5[0] in sqliteDB_query():
            print('信息重复结束')
            break

        # 向sqlite数据库插入数据
        new_data = data + mdbMd5  # 把md5值写入新数据元祖，保存至数据库
        sqlite_sql = """INSERT INTO sim_content ('Content', 'time', 'Simnum', 'Md5') VALUES (?,?,?,?)"""
        i = sqliteDB.execute(sqlite_sql, new_data)  # 数据写入
        print(f'成功写入第：{i}条数据')


if __name__ == '__main__':
    db()