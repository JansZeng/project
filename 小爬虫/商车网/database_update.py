"""
1.刷新md5：品牌表增加了一个新字段real_brand_name，有数据就拿来替换‘品牌名称’重新生成md5，更新商车网数据的md5，同时刷新首字母，没有数据则不更新。
2.合并数据插入新表mergedata：拿MD5匹配成功后用 商车网:vehicle_model_code,vin,brand_name,engine_displacement     汽车之家：车系名称, 级别,能源类型, 变速箱类型
这些字段造一条数据插入新表。
3.mergedata表同样是用公告型号、识别代号组合去重
"""
import pinyin
import pymysql
import hashlib


class DatabaseUpdate:
    def __init__(self):
        self.db = MySql()
        self.md5s = list()

    def update_initial(self):
        """更新 vehicle_brand_info 首字母"""
        # 1:根据real_brand_name字段值 更新vehicle_brand_info表 首字母
        print('更新:vehicle_brand_info表 initial字段 ')
        sql = 'select id,real_brand_name from vehicle_brand_info where real_brand_name!="None"'  # 查询real_brand_name字段有值项
        fetchall = self.db.query(sql)
        if not fetchall:
            print(f'数据没有更新')
            return
        for fetch in fetchall:
            id, real_brand_name = fetch
            # 判断real_brand_name 是否有值
            if not real_brand_name:
                continue
            initial = pinyin.get(real_brand_name).capitalize()[0]  # 新品牌首字母
            create_sql = "update vehicle_brand_info set initial='{}' where id={};".format(initial, id)
            self.db.create(sql=create_sql)  # 更新首字母
            print(f'vehicle_brand_info表 {id} {initial} 数据更新完成')
            # 2:更新 cndatebase md5值
            self.update_md5(id, real_brand_name)
            print(f'成功 更新：{len(self.md5s)} 条数据')
        print(f'vehicle_brand_info表 数据更新完成')

    def update_md5(self, id, real_brand_name):
        """更新 cndatebase md5"""
        # 1:根据real_brand_name字段值 更新vehicle_brand_info表 首字母
        sql = "SELECT id,wheel_base, vehicle_length, vehicle_wide, vehicle_high FROM cndatebase WHERE brand_name={};".format(id)  # 查询real_brand_name字段有值项
        fetchall = self.db.query(sql)
        for fetch in fetchall:
            md5data = ''.join([i.split(',')[0] for i in fetch[1:]]) + real_brand_name
            mdbMd5 = self.updateMd5(md5data)
            # 更新md5
            create_sql = "update cndatebase set md5='{}' where id={};".format(mdbMd5, fetch[0])
            if self.db.create(sql=create_sql):  # cndatebase md5
                self.md5s.append(mdbMd5)

    def updateMd5(self, data):
        # 创建md5对象
        md5obj = hashlib.md5()
        md5obj.update(data.encode(encoding='utf-8'))
        md5code = md5obj.hexdigest()
        return md5code

    def inquire_md5(self):
        """md5 匹配查询"""
        print('MD5 匹配')
        x_sql = "SELECT md5 FROM cndatebase;"
        x_fetchall = self.db.query(sql=x_sql)
        x_fetchall = [i[0] for i in x_fetchall if i]

        for md5 in x_fetchall:
            auto_sql = "SELECT 车系名称,级别,能源类型,变速箱类型 FROM autodatebase WHERE MD5='{}';".format(md5)
            auto_fetchall = self.db.query(auto_sql)
            if not auto_fetchall:
                print(f'md5:{md5}没有匹配到数据')
                continue
            cn_sql = "SELECT vehicle_model_code,vin,brand_name,engine_displacement FROM cndatebase WHERE MD5='{}';".format(md5)
            cn_fetchall = self.db.query(cn_sql)
            mergedatas = [list(i)+list(auto_fetchall[0]) for i in cn_fetchall]
            print(f'成功匹配到：{len(mergedatas)}条数据')
            for mergedata in mergedatas:
                self.create_merge(mergedata=mergedata)

    def create_merge(self, mergedata):
        """mergedata 数据插入"""
        # 公告型号+识别代号 去重
        sql_b = "select vehicle_model_code,vin from mergedata WHERE vehicle_model_code='{}' and vin='{}'".format(mergedata[0], mergedata[1])
        if self.db.query(sql=sql_b):
            print('公告型号+识别代号 去重 数据重复跳过。')
            return
        sql = "INSERT INTO mergedata(vehicle_model_code, vin, brand_id, vehicle_name, level, energy_type, transmission_type, engine_displacement) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        if self.db.create(sql=sql, param=tuple(mergedata)):
            print(f'mergedata表 成功插入一条数据')


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


if __name__ == '__main__':
    spider = DatabaseUpdate()
    spider.update_initial()
    # spider.inquire_md5()
